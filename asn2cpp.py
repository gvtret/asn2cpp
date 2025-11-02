#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
asn2cpp_antlr.py
Auto-generates C++ code (C++11/C++14/C++17) from ASN.1 definitions using ANTLR4 grammar.
Relies on generated parser classes in ./parser (ASNParser, ASNLexer, ASNVisitor).
"""

import sys
import os
import datetime
import re
import argparse
from typing import Dict
from antlr4 import *
from parser.ASNLexer import ASNLexer
from parser.ASNParser import ASNParser
from parser.ASNVisitor import ASNVisitor


# ---------------------------------------------------------------------
# Helper utilities
# ---------------------------------------------------------------------
def iso_datetime():
    """Return current UTC time in ISO-8601 format."""
    return datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")


def header_guard(name: str):
    """Generate include guard from filename."""
    return name.replace(".", "_").replace("-", "_").upper() + "_"


def sanitize_identifier(name: str) -> str:
    """Replace characters that are invalid in C++ identifiers."""
    if not name:
        return ""
    sanitized = re.sub(r"\W", "_", name.strip())
    if sanitized and sanitized[0].isdigit():
        sanitized = f"_{sanitized}"
    if sanitized.lower() in CPP_KEYWORDS:
        sanitized = f"{sanitized}_"
    return sanitized


CPP_KEYWORDS = {
    "alignas",
    "alignof",
    "and",
    "and_eq",
    "asm",
    "auto",
    "bitand",
    "bitor",
    "bool",
    "break",
    "case",
    "catch",
    "char",
    "char16_t",
    "char32_t",
    "class",
    "compl",
    "const",
    "constexpr",
    "const_cast",
    "continue",
    "decltype",
    "default",
    "delete",
    "do",
    "double",
    "dynamic_cast",
    "else",
    "enum",
    "explicit",
    "export",
    "extern",
    "false",
    "float",
    "for",
    "friend",
    "goto",
    "if",
    "inline",
    "int",
    "long",
    "mutable",
    "namespace",
    "new",
    "noexcept",
    "not",
    "not_eq",
    "nullptr",
    "operator",
    "or",
    "or_eq",
    "private",
    "protected",
    "public",
    "register",
    "reinterpret_cast",
    "return",
    "short",
    "signed",
    "sizeof",
    "static",
    "static_assert",
    "static_cast",
    "struct",
    "switch",
    "template",
    "this",
    "thread_local",
    "throw",
    "true",
    "try",
    "typedef",
    "typeid",
    "typename",
    "union",
    "unsigned",
    "using",
    "virtual",
    "void",
    "volatile",
    "wchar_t",
    "while",
    "xor",
    "xor_eq",
}

CONSTRAINT_MARKERS = ("{", "(", "[")


def strip_constraints(asn_type: str) -> str:
    """Remove constraint suffixes such as {...}, (...) or [...]."""
    if not asn_type:
        return ""
    cut_positions = [
        pos
        for marker in CONSTRAINT_MARKERS
        for pos in [asn_type.find(marker)]
        if pos != -1
    ]
    if not cut_positions:
        return asn_type
    return asn_type[: min(cut_positions)]


def normalize_type_name(asn_type: str) -> str:
    """Strip constraints and sanitize an ASN.1 type reference."""
    base = strip_constraints(asn_type)
    return sanitize_identifier(base.strip())


def type_key(asn_type: str) -> str:
    """Return a canonical lookup key for type mapping."""
    base = strip_constraints(asn_type)
    if not base:
        return ""
    base = base.replace("-", " ")
    base = base.replace("_", " ")
    base = re.sub(r"\s+", " ", base).strip()
    return base.upper()


def cpp_type(
    asn_type: str, *, null_type: str = "NullType", use_variant: bool = False
) -> str:
    """Rough mapping from ASN.1 type to C++ type."""
    type_map = {
        "INTEGER": "int",
        "BOOLEAN": "bool",
        "OCTET STRING": "std::vector<uint8_t>",
        "OCTETSTRING": "std::vector<uint8_t>",
        "BIT STRING": "std::vector<bool>",
        "BITSTRING": "std::vector<bool>",
        "VISIBLESTRING": "std::string",
        "UTF8STRING": "std::string",
        "GRAPHICSTRING": "std::string",
        "IA5STRING": "std::string",
        "PRINTABLESTRING": "std::string",
        "NUMERICSTRING": "std::string",
        "GENERALIZEDTIME": "std::string",
        "UTCTIME": "std::string",
        "ENUMERATED": "int",
        "SEQUENCE": "std::vector<uint8_t>",
        "NULL": null_type,
        "OBJECT IDENTIFIER": "std::vector<int>",
        "OBJECTIDENTIFIER": "std::vector<int>",
    }
    if use_variant:
        type_map["CHOICE"] = f"std::variant<{null_type}>"
    else:
        type_map["CHOICE"] = null_type
    key = type_key(asn_type)
    return type_map.get(key, sanitize_identifier(normalize_type_name(asn_type)))


# ---------------------------------------------------------------------
# Visitor that generates C++ code
# ---------------------------------------------------------------------
class CppGenerator(ASNVisitor):
    def __init__(
        self,
        module_name,
        *,
        generate_cpp: bool = True,
        overwrite_cpp: bool = False,
        output_dir: str = ".",
        cpp_standard: str = "c++17",
    ):
        self.module_name = module_name
        self.types = []
        self.enums = []
        self.choices = []
        self.simple_types = []
        self.sequence_of = []
        self.type_kinds: Dict[str, str] = {}
        self.inline_names: Dict[int, str] = {}
        self.inline_counter = 0
        self.generate_cpp = generate_cpp
        self.overwrite_cpp = overwrite_cpp
        self.output_dir = os.path.abspath(output_dir or ".")
        self.cpp_standard = cpp_standard
        self.use_variant = cpp_standard == "c++17"
        self.null_type = "std::monostate" if self.use_variant else "NullType"

    # --- TypeAssignment ------------------------------------------------
    def visitTypeAssignment(self, ctx):
        # Try to extract type name from the parent assignment context
        name = None
        parent = getattr(ctx, "parentCtx", None)
        if parent and hasattr(parent, "IDENTIFIER"):
            ident = parent.IDENTIFIER()
            if ident:
                name = ident.getText()
        if not name:
            # Fallback to scanning the children for an identifier token
            for c in ctx.getChildren():
                token_text = str(c)
                if token_text.isidentifier():
                    name = token_text
                    break
        if not name:
            name = "AnonymousType"
        name = sanitize_identifier(name)

        asn = ctx.asnType()
        builtin = asn.builtinType() if asn and hasattr(asn, "builtinType") else None
        defined = asn.definedType() if asn and hasattr(asn, "definedType") else None
        if builtin and builtin.sequenceType():
            self.types.append((name, builtin.sequenceType()))
            self.type_kinds[name] = "sequence"
        elif (
            builtin
            and getattr(builtin, "sequenceOfType", None)
            and builtin.sequenceOfType()
        ):
            self.sequence_of.append((name, builtin.sequenceOfType()))
            self.type_kinds[name] = "sequence_of"
        elif builtin and builtin.enumeratedType():
            self.enums.append((name, builtin.enumeratedType()))
            self.type_kinds[name] = "enum"
        elif builtin and builtin.choiceType():
            self.choices.append((name, builtin.choiceType()))
            self.type_kinds[name] = "choice"
        else:
            target = ""
            if builtin:
                target = builtin.getText()
            elif defined:
                target = defined.getText()
            else:
                target = asn.getText() if asn else ""
            self.simple_types.append((name, target))
            self.type_kinds[name] = "alias"
        return self.visitChildren(ctx)

    # --- Helpers --------------------------------------------------------
    def _unique_inline_name(self, base: str) -> str:
        candidate = sanitize_identifier(base) or f"InlineType{self.inline_counter}"
        name = candidate
        suffix = 1
        while name in self.type_kinds:
            name = f"{candidate}_{suffix}"
            suffix += 1
        self.inline_counter += 1
        return name

    def _cache_inline(self, ctx, name: str, kind: str):
        key = id(ctx)
        cached = self.inline_names.get(key)
        if cached:
            return cached
        self.inline_names[key] = name
        if kind == "sequence":
            self.types.append((name, ctx))
        elif kind == "choice":
            self.choices.append((name, ctx))
        elif kind == "enum":
            self.enums.append((name, ctx))
        self.type_kinds[name] = kind
        return name

    def _ensure_inline_sequence(self, owner: str, ctx):
        key = id(ctx)
        if key in self.inline_names:
            return self.inline_names[key]
        name = self._unique_inline_name(f"{owner}_Sequence")
        return self._cache_inline(ctx, name, "sequence")

    @staticmethod
    def _safe_identifier(name: str, fallback: str) -> str:
        candidate = sanitize_identifier(name) or fallback
        if candidate[0].isdigit():
            candidate = f"_{candidate}"
        return candidate

    @staticmethod
    def _unique_choice_token(base: str, existing: set, fallback: str) -> str:
        candidate = CppGenerator._safe_identifier(base, fallback)
        original = candidate
        suffix = 1
        while candidate in existing:
            candidate = f"{original}_{suffix}"
            suffix += 1
        existing.add(candidate)
        return candidate

    def _ensure_inline_choice(self, owner: str, ctx):
        key = id(ctx)
        if key in self.inline_names:
            return self.inline_names[key]
        name = self._unique_inline_name(f"{owner}_Choice")
        return self._cache_inline(ctx, name, "choice")

    def _ensure_inline_enum(self, owner: str, ctx):
        key = id(ctx)
        if key in self.inline_names:
            return self.inline_names[key]
        name = self._unique_inline_name(f"{owner}_Enum")
        return self._cache_inline(ctx, name, "enum")

    def _wrap_defined(self, name: str, usage: str) -> str:
        if usage == "alias":
            return name
        kind = self.type_kinds.get(name)
        if kind in {"sequence", "choice", "sequence_of"}:
            return f"std::shared_ptr<{name}>"
        return name

    def render_type_from_ctx(self, asn_type_ctx, usage: str, owner: str) -> str:
        if asn_type_ctx is None:
            return self.null_type
        if hasattr(asn_type_ctx, "definedType") and asn_type_ctx.definedType():
            target = normalize_type_name(asn_type_ctx.definedType().getText())
            return self._wrap_defined(target, usage)
        if hasattr(asn_type_ctx, "referencedType") and asn_type_ctx.referencedType():
            ref = asn_type_ctx.referencedType()
            if ref.definedType():
                text = ref.definedType().getText()
                mapped = cpp_type(
                    text, null_type=self.null_type, use_variant=self.use_variant
                )
                normalized = normalize_type_name(text)
                if mapped and mapped != normalized:
                    return mapped
                return self._wrap_defined(normalized, usage)
            text = ref.getText()
            normalized = normalize_type_name(text)
            if normalized in self.type_kinds:
                return self._wrap_defined(normalized, usage)
            mapped = cpp_type(
                text, null_type=self.null_type, use_variant=self.use_variant
            )
            if mapped and mapped != normalized:
                return mapped
            return normalized
        builtin = (
            asn_type_ctx.builtinType() if hasattr(asn_type_ctx, "builtinType") else None
        )
        if not builtin:
            return cpp_type(
                asn_type_ctx.getText(),
                null_type=self.null_type,
                use_variant=self.use_variant,
            )
        if getattr(builtin, "sequenceOfType", None) and builtin.sequenceOfType():
            seq_of = builtin.sequenceOfType()
            element_ctx = seq_of.asnType()
            if not element_ctx and seq_of.namedType():
                element_ctx = seq_of.namedType().asnType()
            element_type = self.render_type_from_ctx(
                element_ctx, "sequence_element", owner
            )
            if not element_type:
                element_type = self.null_type
            return f"std::vector<{element_type}>"
        if builtin.choiceType():
            inline_name = self._ensure_inline_choice(owner, builtin.choiceType())
            return self._wrap_defined(inline_name, usage)
        if builtin.sequenceType():
            inline_name = self._ensure_inline_sequence(owner, builtin.sequenceType())
            return self._wrap_defined(inline_name, usage)
        if builtin.enumeratedType():
            inline_name = self._ensure_inline_enum(owner, builtin.enumeratedType())
            return self._wrap_defined(inline_name, usage)
        return cpp_type(
            builtin.getText(), null_type=self.null_type, use_variant=self.use_variant
        )

    def render_reference_from_text(self, text: str, usage: str, owner: str) -> str:
        key = type_key(text)
        mapped = cpp_type(text, null_type=self.null_type, use_variant=self.use_variant)
        if key in {
            "INTEGER",
            "BOOLEAN",
            "OCTET STRING",
            "OCTETSTRING",
            "BIT STRING",
            "BITSTRING",
            "VISIBLESTRING",
            "UTF8STRING",
            "GRAPHICSTRING",
            "IA5STRING",
            "PRINTABLESTRING",
            "NUMERICSTRING",
            "GENERALIZEDTIME",
            "UTCTIME",
            "ENUMERATED",
            "CHOICE",
            "SEQUENCE",
            "NULL",
            "OBJECT IDENTIFIER",
            "OBJECTIDENTIFIER",
        }:
            return mapped
        if "SEQUENCE" in key and "OF" in key:
            parts = text.split("OF", 1)
            element = parts[1] if len(parts) > 1 else self.null_type
            element_type = self.render_reference_from_text(
                element, "sequence_element", owner
            )
            return f"std::vector<{element_type}>"
        normalized = normalize_type_name(text)
        if normalized in self.type_kinds:
            return self._wrap_defined(normalized, usage)
        return self._wrap_defined(normalized, usage)

    def _prepare_inline_types(self):
        # Force discovery of inline types before emitting declarations.
        for name, seq_ctx in list(self.types):
            if not seq_ctx.componentTypeLists():
                continue
            comp_lists = seq_ctx.componentTypeLists().rootComponentTypeList()
            if not isinstance(comp_lists, (list, tuple)):
                comp_lists = [comp_lists]
            for comp_list in comp_lists:
                if not comp_list:
                    continue
                ct_list = comp_list.componentTypeList()
                if not ct_list:
                    continue
                for comp in ct_list.componentType():
                    named = comp.namedType()
                    if not named or not named.asnType():
                        continue
                    field_name = (
                        sanitize_identifier(named.IDENTIFIER().getText())
                        if named.IDENTIFIER()
                        else "field"
                    )
                    self.render_type_from_ctx(
                        named.asnType(), "field", f"{name}_{field_name}"
                    )
        for name, ch_ctx in list(self.choices):
            if not ch_ctx.alternativeTypeLists():
                continue
            root_alts = ch_ctx.alternativeTypeLists().rootAlternativeTypeList()
            if not isinstance(root_alts, (list, tuple)):
                root_alts = [root_alts]
            for root_alt in root_alts:
                if not root_alt:
                    continue
                alt_list = root_alt.alternativeTypeList()
                if not alt_list:
                    continue
                for idx, alt in enumerate(alt_list.namedType()):
                    if not alt.asnType():
                        continue
                    alt_name = (
                        alt.IDENTIFIER().getText() if alt.IDENTIFIER() else f"alt_{idx}"
                    )
                    self.render_type_from_ctx(
                        alt.asnType(),
                        "variant",
                        f"{name}_{sanitize_identifier(alt_name)}",
                    )
        for name, seq_ctx in list(self.sequence_of):
            element_ctx = seq_ctx.asnType()
            if not element_ctx and seq_ctx.namedType():
                element_ctx = seq_ctx.namedType().asnType()
            self.render_type_from_ctx(
                element_ctx, "sequence_element", f"{name}_element"
            )

    def _collect_function_specs(self):
        specs = []
        for name, _ in self.types:
            specs.append(
                {
                    "key": f"{name}::encode",
                    "signature": f"std::vector<uint8_t> {name}::encode() const",
                    "return_type": "std::vector<uint8_t>",
                    "type_name": name,
                    "method": "encode",
                    "body": [
                        "  // TODO: implement ASN.1 DER/BER encoder",
                        "  return {};",
                    ],
                }
            )
            specs.append(
                {
                    "key": f"{name}::decode",
                    "signature": f"bool {name}::decode(const std::vector<uint8_t>& data)",
                    "return_type": "bool",
                    "type_name": name,
                    "method": "decode",
                    "body": [
                        "  // TODO: implement ASN.1 DER/BER decoder",
                        "  (void)data; return true;",
                    ],
                }
            )
        for name, _ in self.choices:
            specs.append(
                {
                    "key": f"{name}::encode",
                    "signature": f"std::vector<uint8_t> {name}::encode() const",
                    "return_type": "std::vector<uint8_t>",
                    "type_name": name,
                    "method": "encode",
                    "body": [
                        "  // TODO: implement ASN.1 DER/BER encoder",
                        "  return {};",
                    ],
                }
            )
            specs.append(
                {
                    "key": f"{name}::decode",
                    "signature": f"bool {name}::decode(const std::vector<uint8_t>& data)",
                    "return_type": "bool",
                    "type_name": name,
                    "method": "decode",
                    "body": [
                        "  // TODO: implement ASN.1 DER/BER decoder",
                        "  (void)data; return true;",
                    ],
                }
            )
        return specs

    def _merge_with_existing_cpp(self, cpp_path: str, function_specs):
        with open(cpp_path, "r", encoding="utf-8") as f:
            original_lines = f.read().splitlines()

        lines = original_lines[:]
        handled = set()
        changed = False

        for spec in function_specs:
            exact_pattern = re.compile(
                rf"^\s*{re.escape(spec['return_type'])}\s+{re.escape(spec['type_name'])}::{spec['method']}\s*\("
            )
            fallback_pattern = re.compile(
                rf"^(\s*).{{0,120}}{re.escape(spec['type_name'])}::{spec['method']}\s*\("
            )
            desired = f"{spec['signature']} {{"
            for idx, line in enumerate(lines):
                if exact_pattern.match(line):
                    handled.add(spec["key"])
                    indent = re.match(r"^(\s*)", line).group(1)
                    if line.strip() != desired:
                        lines[idx] = indent + desired
                        changed = True
                    elif not line.rstrip().endswith("{"):
                        lines[idx] = indent + desired
                        changed = True
                    break
            else:
                for idx, line in enumerate(lines):
                    match = fallback_pattern.match(line)
                    if match:
                        handled.add(spec["key"])
                        indent = match.group(1)
                        lines[idx] = indent + desired
                        changed = True
                        break

        missing_specs = [spec for spec in function_specs if spec["key"] not in handled]
        if missing_specs:
            changed = True
            insert_index = None
            for idx, line in enumerate(lines):
                if line.strip() == "} // namespace DLMS":
                    insert_index = idx
                    break
            if insert_index is None:
                insert_index = len(lines)
            insertion = []
            if insert_index > 0 and lines[insert_index - 1].strip():
                insertion.append("")
            for spec in missing_specs:
                insertion.append(f"{spec['signature']} {{")
                insertion.extend(spec["body"])
                insertion.append("}")
                insertion.append("")
            if insertion and insertion[-1] == "":
                insertion.pop()
            lines[insert_index:insert_index] = insertion

        if changed:
            with open(cpp_path, "w", encoding="utf-8") as f:
                f.write("\n".join(lines) + "\n")
            return "updated"
        return "unchanged"

    # --- SEQUENCE ------------------------------------------------------
    def visitSequenceType(self, ctx):
        # handled in visitTypeAssignment
        return None

    # --- CHOICE --------------------------------------------------------
    def visitChoiceType(self, ctx):
        # handled in visitTypeAssignment
        return None

    # --- ENUMERATED ----------------------------------------------------
    def visitEnumeratedType(self, ctx):
        # handled in visitTypeAssignment
        return None

    # ------------------------------------------------------------------
    def generate(self):
        hpp_name = f"{self.module_name}.hpp"
        cpp_name = f"{self.module_name}.cpp"
        hpp_path = os.path.join(self.output_dir, hpp_name)
        cpp_path = os.path.join(self.output_dir, cpp_name)
        guard = header_guard(hpp_name)
        date_str = iso_datetime()

        # Ensure inline types are registered before emitting code.
        self._prepare_inline_types()

        # --- HEADER FILE ---
        hpp = []
        hpp.append(f"/**")
        hpp.append(f" * @file {hpp_name}")
        hpp.append(
            f" * @brief Auto-generated C++ types from ASN.1 module {self.module_name}"
        )
        hpp.append(f" * @date {date_str}")
        hpp.append(f" * @note Target C++ standard: {self.cpp_standard}")
        hpp.append(f" * @generated by asn2cpp_antlr.py")
        hpp.append(f" */\n")
        hpp.append(f"#ifndef {guard}")
        hpp.append(f"#define {guard}\n")
        hpp.append("#include <string>")
        hpp.append("#include <vector>")
        if self.use_variant:
            hpp.append("#include <variant>")
        hpp.append("#include <memory>")
        hpp.append("#include <cstdint>\n")
        hpp.append("namespace DLMS {\n")

        if self.null_type == "NullType":
            hpp.append(
                "/** @brief Placeholder type for ASN.1 NULL when std::monostate is unavailable */"
            )
            hpp.append("struct NullType {};")
            hpp.append("")

        # --- FORWARD DECLARATIONS ---
        for name, _ in list(self.types) + list(self.choices):
            hpp.append(f"struct {name};")
        if self.types or self.choices:
            hpp.append("")

        # --- SIMPLE TYPE ALIASES ---
        for name, target in self.simple_types:
            resolved = self.render_reference_from_text(target, "alias", name)
            doc_target = strip_constraints(target).strip() or target
            hpp.append(f"/** @brief TYPE {name} aliases ASN.1 {doc_target} */")
            hpp.append(f"using {name} = {resolved};\n")

        # --- SEQUENCE OF TYPES ---
        for name, seq_ctx in self.sequence_of:
            element_ctx = seq_ctx.asnType()
            if not element_ctx and seq_ctx.namedType():
                element_ctx = seq_ctx.namedType().asnType()
            element_type = self.render_type_from_ctx(
                element_ctx, "sequence_element", f"{name}_element"
            )
            doc_target = seq_ctx.getText()
            hpp.append(f"/** @brief TYPE {name} aliases ASN.1 {doc_target} */")
            hpp.append(f"using {name} = std::vector<{element_type}>;\n")

        # --- ENUMERATED TYPES ---
        for name, enum_ctx in self.enums:
            hpp.append(f"/** @brief ENUMERATED type {name} */")
            hpp.append(f"enum class {name} {{")
            items = []
            if enum_ctx.enumerations() and enum_ctx.enumerations().rootEnumeration():
                enumeration = enum_ctx.enumerations().rootEnumeration().enumeration()
                if enumeration:
                    for item_ctx in enumeration.enumerationItem():
                        ident = None
                        if item_ctx.IDENTIFIER():
                            ident = item_ctx.IDENTIFIER().getText()
                        elif (
                            item_ctx.namedNumber()
                            and item_ctx.namedNumber().IDENTIFIER()
                        ):
                            ident = item_ctx.namedNumber().IDENTIFIER().getText()
                        elif item_ctx.value():
                            ident = item_ctx.value().getText()
                        if not ident:
                            ident = "Unnamed"
                        items.append(f"  {sanitize_identifier(ident)}")
            if items:
                hpp.append(",\n".join(items))
            hpp.append("};\n")

        # --- SEQUENCE TYPES ---
        for name, seq_ctx in self.types:
            hpp.append(f"/** @brief SEQUENCE type {name} */")
            hpp.append(f"struct {name} {{")
            if seq_ctx.componentTypeLists():
                comp_lists = seq_ctx.componentTypeLists().rootComponentTypeList()
                if not isinstance(comp_lists, (list, tuple)):
                    comp_lists = [comp_lists]
                for comp_list in comp_lists:
                    if not comp_list:
                        continue
                    ct_list = comp_list.componentTypeList()
                    if not ct_list:
                        continue
                    for comp in ct_list.componentType():
                        named = comp.namedType()
                        if not named:
                            continue
                        if not named.IDENTIFIER():
                            continue
                        field_name = sanitize_identifier(named.IDENTIFIER().getText())
                        field_type = named.asnType().getText()
                        cpp_field_type = self.render_type_from_ctx(
                            named.asnType(), "field", f"{name}_{field_name}"
                        )
                        hpp.append(
                            f"  /** @brief Field {field_name} of type {field_type} */"
                        )
                        hpp.append(f"  {cpp_field_type} {field_name};")
            hpp.append("")
            hpp.append("  /** @brief Encode this structure to ASN.1 binary form */")
            hpp.append("  std::vector<uint8_t> encode() const;")
            hpp.append("  /** @brief Decode this structure from ASN.1 binary form */")
            hpp.append("  bool decode(const std::vector<uint8_t>& data);")
            hpp.append("};\n")

        # --- CHOICE TYPES ---
        for name, ch_ctx in self.choices:
            hpp.append(f"/** @brief CHOICE type {name} */")
            hpp.append(f"struct {name} {{")
            alternatives = []
            enum_tokens = set()
            field_tokens = set()
            if ch_ctx.alternativeTypeLists():
                root_alts = ch_ctx.alternativeTypeLists().rootAlternativeTypeList()
                if not isinstance(root_alts, (list, tuple)):
                    root_alts = [root_alts]
                for root_alt in root_alts:
                    if not root_alt:
                        continue
                    alt_list = root_alt.alternativeTypeList()
                    if not alt_list:
                        continue
                    for idx, alt in enumerate(alt_list.namedType()):
                        if not alt.asnType():
                            continue
                        raw_label = (
                            alt.IDENTIFIER().getText()
                            if alt.IDENTIFIER()
                            else f"Alternative{idx}"
                        )
                        enum_name = self._unique_choice_token(
                            raw_label, enum_tokens, f"Alternative{idx}"
                        )
                        field_name = self._unique_choice_token(
                            f"{enum_name}_value",
                            field_tokens,
                            f"alternative_{idx}_value",
                        )
                        field_type = self.render_type_from_ctx(
                            alt.asnType(),
                            "variant",
                            f"{name}_{enum_name}",
                        )
                        alternatives.append(
                            {
                                "enum": enum_name,
                                "field": field_name,
                                "type": field_type,
                                "doc": alt.asnType().getText(),
                                "label": raw_label,
                            }
                        )
            if self.use_variant:
                hpp.append("  /** @brief Variant of all possible alternatives */")
                variant_alts = [alt["type"] for alt in alternatives] or [self.null_type]
                variant_decl = "std::variant<" + ", ".join(variant_alts) + ">"
                hpp.append(f"  {variant_decl} value;")
            else:
                hpp.append(
                    "  /** @brief Indicates which CHOICE alternative is active. */"
                )
                hpp.append("  enum class Kind {")
                enum_entries = ["    None"] + [
                    f"    {alt['enum']}" for alt in alternatives
                ]
                hpp.append(",\n".join(enum_entries))
                hpp.append("  };")
                hpp.append("  Kind kind = Kind::None;")
                if alternatives:
                    hpp.append("")
                    for alt in alternatives:
                        doc_label = alt["label"] or alt["enum"]
                        hpp.append(
                            f"  /** @brief Alternative {doc_label} of type {alt['doc']} */"
                        )
                        hpp.append(f"  {alt['type']} {alt['field']};")
            hpp.append("")
            hpp.append("  std::vector<uint8_t> encode() const;")
            hpp.append("  bool decode(const std::vector<uint8_t>& data);")
            hpp.append("};\n")

        hpp.append("} // namespace DLMS\n")
        hpp.append(f"#endif // {guard}\n")

        # --- CPP FILE ---
        cpp = []
        function_specs = self._collect_function_specs()

        if self.generate_cpp:
            cpp.append(f"/**")
            cpp.append(f" * @file {cpp_name}")
            cpp.append(
                f" * @brief Implementation of encode/decode for ASN.1 module {self.module_name}"
            )
            cpp.append(f" * @date {date_str}")
            cpp.append(f" * @note Target C++ standard: {self.cpp_standard}")
            cpp.append(f" * @generated by asn2cpp_antlr.py")
            cpp.append(f" */\n")
            cpp.append(f'#include "{hpp_name}"')
            cpp.append("namespace DLMS {\n")
            for idx, spec in enumerate(function_specs):
                cpp.append(f"{spec['signature']} {{")
                cpp.extend(spec["body"])
                cpp.append("}")
                if idx != len(function_specs) - 1:
                    cpp.append("")
            cpp.append("} // namespace DLMS\n")

        # --- Write files ---
        os.makedirs(self.output_dir, exist_ok=True)

        with open(hpp_path, "w", encoding="utf-8") as f:
            f.write("\n".join(hpp))
        message = [f"Generated: {hpp_path}"]
        if self.generate_cpp:
            if os.path.exists(cpp_path) and not self.overwrite_cpp:
                status = self._merge_with_existing_cpp(cpp_path, function_specs)
                if status == "updated":
                    message.append(
                        f"Updated {cpp_path} with new or revised method stubs."
                    )
                else:
                    message.append(
                        f"Preserved existing {cpp_path}; use --overwrite-cpp to regenerate."
                    )
            else:
                with open(cpp_path, "w", encoding="utf-8") as f:
                    f.write("\n".join(cpp))
                message[0] = f"Generated: {hpp_path}, {cpp_path}"
        else:
            if os.path.exists(cpp_path):
                message.append(f"Skipped regeneration of existing {cpp_path}.")
            else:
                message.append(f"Skipped cpp generation; {cpp_path} not created.")
        print(" ".join(message))


# ---------------------------------------------------------------------
# Main entry
# ---------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(
        description="Generate C++ code from ASN.1 definitions using ANTLR4."
    )
    parser.add_argument("input", help="Path to ASN.1 module file")
    parser.add_argument(
        "--header-only",
        action="store_true",
        help="Generate only the header file and keep existing implementation files.",
    )
    parser.add_argument(
        "--overwrite-cpp",
        action="store_true",
        help="Regenerate the cpp file even if it already exists.",
    )
    parser.add_argument(
        "-o",
        "--output-dir",
        default=".",
        help="Directory where generated files will be written.",
    )
    parser.add_argument(
        "--cpp-standard",
        choices=["c++11", "c++14", "c++17"],
        default="c++17",
        help="C++ standard to target in the generated output.",
    )
    args = parser.parse_args()

    input_file = args.input
    module_name = os.path.splitext(os.path.basename(input_file))[0]

    input_stream = FileStream(input_file, encoding="utf-8")
    lexer = ASNLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = ASNParser(stream)
    tree = parser.moduleDefinition()

    visitor = CppGenerator(
        module_name,
        generate_cpp=not args.header_only,
        overwrite_cpp=args.overwrite_cpp,
        output_dir=args.output_dir,
        cpp_standard=args.cpp_standard,
    )
    visitor.visit(tree)
    visitor.generate()


if __name__ == "__main__":
    main()
