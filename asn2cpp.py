#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
asn2cpp_antlr.py
Auto-generates C++11 code from ASN.1 definitions using ANTLR4 grammar.
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
        return name
    return name.replace("-", "_")


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


def cpp_type(asn_type: str) -> str:
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
        "CHOICE": "std::variant<std::monostate>",
        "SEQUENCE": "std::vector<uint8_t>",
        "NULL": "std::monostate",
        "OBJECT IDENTIFIER": "std::vector<int>",
        "OBJECTIDENTIFIER": "std::vector<int>",
    }
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
            return "std::monostate"
        if hasattr(asn_type_ctx, "definedType") and asn_type_ctx.definedType():
            target = normalize_type_name(asn_type_ctx.definedType().getText())
            return self._wrap_defined(target, usage)
        if hasattr(asn_type_ctx, "referencedType") and asn_type_ctx.referencedType():
            ref = asn_type_ctx.referencedType()
            if ref.definedType():
                text = ref.definedType().getText()
                mapped = cpp_type(text)
                normalized = normalize_type_name(text)
                if mapped and mapped != normalized:
                    return mapped
                return self._wrap_defined(normalized, usage)
            text = ref.getText()
            normalized = normalize_type_name(text)
            if normalized in self.type_kinds:
                return self._wrap_defined(normalized, usage)
            mapped = cpp_type(text)
            if mapped and mapped != normalized:
                return mapped
            return normalized
        builtin = (
            asn_type_ctx.builtinType() if hasattr(asn_type_ctx, "builtinType") else None
        )
        if not builtin:
            return cpp_type(asn_type_ctx.getText())
        if getattr(builtin, "sequenceOfType", None) and builtin.sequenceOfType():
            seq_of = builtin.sequenceOfType()
            element_ctx = seq_of.asnType()
            if not element_ctx and seq_of.namedType():
                element_ctx = seq_of.namedType().asnType()
            element_type = self.render_type_from_ctx(
                element_ctx, "sequence_element", owner
            )
            if not element_type:
                element_type = "std::monostate"
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
        return cpp_type(builtin.getText())

    def render_reference_from_text(self, text: str, usage: str, owner: str) -> str:
        key = type_key(text)
        mapped = cpp_type(text)
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
            element = parts[1] if len(parts) > 1 else "std::monostate"
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
        hpp.append(f" * @generated by asn2cpp_antlr.py")
        hpp.append(f" */\n")
        hpp.append(f"#ifndef {guard}")
        hpp.append(f"#define {guard}\n")
        hpp.append("#include <string>")
        hpp.append("#include <vector>")
        hpp.append("#include <variant>")
        hpp.append("#include <memory>")
        hpp.append("#include <cstdint>\n")
        hpp.append("namespace DLMS {\n")

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
            hpp.append("  /** @brief Variant of all possible alternatives */")
            alts = []
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
                    for alt in alt_list.namedType():
                        if not alt.asnType():
                            continue
                        alt_name = (
                            alt.IDENTIFIER().getText()
                            if alt.IDENTIFIER()
                            else f"alt_{len(alts)}"
                        )
                        field_type = self.render_type_from_ctx(
                            alt.asnType(),
                            "variant",
                            f"{name}_{sanitize_identifier(alt_name)}",
                        )
                        alts.append(field_type)
            if not alts:
                alts.append("std::monostate")
            variant_decl = "std::variant<" + ", ".join(alts) + ">"
            hpp.append(f"  {variant_decl} value;")
            hpp.append("")
            hpp.append("  std::vector<uint8_t> encode() const;")
            hpp.append("  bool decode(const std::vector<uint8_t>& data);")
            hpp.append("};\n")

        hpp.append("} // namespace DLMS\n")
        hpp.append(f"#endif // {guard}\n")

        # --- CPP FILE ---
        cpp = []
        if self.generate_cpp:
            cpp.append(f"/**")
            cpp.append(f" * @file {cpp_name}")
            cpp.append(
                f" * @brief Implementation of encode/decode for ASN.1 module {self.module_name}"
            )
            cpp.append(f" * @date {date_str}")
            cpp.append(f" * @generated by asn2cpp_antlr.py")
            cpp.append(f" */\n")
            cpp.append(f'#include "{hpp_name}"')
            cpp.append("namespace DLMS {\n")
            for name, seq_ctx in self.types:
                cpp.append(f"std::vector<uint8_t> {name}::encode() const {{")
                cpp.append("  // TODO: implement ASN.1 DER/BER encoder")
                cpp.append("  return {};")
                cpp.append("}\n")
                cpp.append(f"bool {name}::decode(const std::vector<uint8_t>& data) {{")
                cpp.append("  // TODO: implement ASN.1 DER/BER decoder")
                cpp.append("  (void)data; return true;")
                cpp.append("}\n")
            cpp.append("} // namespace DLMS\n")

        # --- Write files ---
        os.makedirs(self.output_dir, exist_ok=True)

        with open(hpp_path, "w", encoding="utf-8") as f:
            f.write("\n".join(hpp))
        message = [f"Generated: {hpp_path}"]
        if self.generate_cpp:
            if os.path.exists(cpp_path) and not self.overwrite_cpp:
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
    )
    visitor.visit(tree)
    visitor.generate()


if __name__ == "__main__":
    main()
