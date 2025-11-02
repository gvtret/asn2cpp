# Generated from ASN.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .ASNParser import ASNParser
else:
    from ASNParser import ASNParser

# This class defines a complete generic visitor for a parse tree produced by ASNParser.

class ASNVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by ASNParser#modules.
    def visitModules(self, ctx:ASNParser.ModulesContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ASNParser#moduleDefinition.
    def visitModuleDefinition(self, ctx:ASNParser.ModuleDefinitionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ASNParser#tagDefault.
    def visitTagDefault(self, ctx:ASNParser.TagDefaultContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ASNParser#extensionDefault.
    def visitExtensionDefault(self, ctx:ASNParser.ExtensionDefaultContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ASNParser#moduleBody.
    def visitModuleBody(self, ctx:ASNParser.ModuleBodyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ASNParser#exports.
    def visitExports(self, ctx:ASNParser.ExportsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ASNParser#symbolsExported.
    def visitSymbolsExported(self, ctx:ASNParser.SymbolsExportedContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ASNParser#imports.
    def visitImports(self, ctx:ASNParser.ImportsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ASNParser#symbolsImported.
    def visitSymbolsImported(self, ctx:ASNParser.SymbolsImportedContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ASNParser#symbolsFromModuleList.
    def visitSymbolsFromModuleList(self, ctx:ASNParser.SymbolsFromModuleListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ASNParser#symbolsFromModule.
    def visitSymbolsFromModule(self, ctx:ASNParser.SymbolsFromModuleContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ASNParser#globalModuleReference.
    def visitGlobalModuleReference(self, ctx:ASNParser.GlobalModuleReferenceContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ASNParser#assignedIdentifier.
    def visitAssignedIdentifier(self, ctx:ASNParser.AssignedIdentifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ASNParser#symbolList.
    def visitSymbolList(self, ctx:ASNParser.SymbolListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ASNParser#symbol.
    def visitSymbol(self, ctx:ASNParser.SymbolContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ASNParser#assignmentList.
    def visitAssignmentList(self, ctx:ASNParser.AssignmentListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ASNParser#assignment.
    def visitAssignment(self, ctx:ASNParser.AssignmentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ASNParser#sequenceType.
    def visitSequenceType(self, ctx:ASNParser.SequenceTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ASNParser#extensionAndException.
    def visitExtensionAndException(self, ctx:ASNParser.ExtensionAndExceptionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ASNParser#optionalExtensionMarker.
    def visitOptionalExtensionMarker(self, ctx:ASNParser.OptionalExtensionMarkerContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ASNParser#componentTypeLists.
    def visitComponentTypeLists(self, ctx:ASNParser.ComponentTypeListsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ASNParser#rootComponentTypeList.
    def visitRootComponentTypeList(self, ctx:ASNParser.RootComponentTypeListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ASNParser#componentTypeList.
    def visitComponentTypeList(self, ctx:ASNParser.ComponentTypeListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ASNParser#componentType.
    def visitComponentType(self, ctx:ASNParser.ComponentTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ASNParser#extensionAdditions.
    def visitExtensionAdditions(self, ctx:ASNParser.ExtensionAdditionsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ASNParser#extensionAdditionList.
    def visitExtensionAdditionList(self, ctx:ASNParser.ExtensionAdditionListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ASNParser#extensionAddition.
    def visitExtensionAddition(self, ctx:ASNParser.ExtensionAdditionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ASNParser#extensionAdditionGroup.
    def visitExtensionAdditionGroup(self, ctx:ASNParser.ExtensionAdditionGroupContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ASNParser#versionNumber.
    def visitVersionNumber(self, ctx:ASNParser.VersionNumberContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ASNParser#sequenceOfType.
    def visitSequenceOfType(self, ctx:ASNParser.SequenceOfTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ASNParser#sizeConstraint.
    def visitSizeConstraint(self, ctx:ASNParser.SizeConstraintContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ASNParser#parameterizedAssignment.
    def visitParameterizedAssignment(self, ctx:ASNParser.ParameterizedAssignmentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ASNParser#parameterList.
    def visitParameterList(self, ctx:ASNParser.ParameterListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ASNParser#parameter.
    def visitParameter(self, ctx:ASNParser.ParameterContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ASNParser#paramGovernor.
    def visitParamGovernor(self, ctx:ASNParser.ParamGovernorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ASNParser#governor.
    def visitGovernor(self, ctx:ASNParser.GovernorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ASNParser#objectClassAssignment.
    def visitObjectClassAssignment(self, ctx:ASNParser.ObjectClassAssignmentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ASNParser#objectClass.
    def visitObjectClass(self, ctx:ASNParser.ObjectClassContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ASNParser#definedObjectClass.
    def visitDefinedObjectClass(self, ctx:ASNParser.DefinedObjectClassContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ASNParser#usefulObjectClassReference.
    def visitUsefulObjectClassReference(self, ctx:ASNParser.UsefulObjectClassReferenceContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ASNParser#externalObjectClassReference.
    def visitExternalObjectClassReference(self, ctx:ASNParser.ExternalObjectClassReferenceContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ASNParser#objectClassDefn.
    def visitObjectClassDefn(self, ctx:ASNParser.ObjectClassDefnContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ASNParser#withSyntaxSpec.
    def visitWithSyntaxSpec(self, ctx:ASNParser.WithSyntaxSpecContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ASNParser#syntaxList.
    def visitSyntaxList(self, ctx:ASNParser.SyntaxListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ASNParser#tokenOrGroupSpec.
    def visitTokenOrGroupSpec(self, ctx:ASNParser.TokenOrGroupSpecContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ASNParser#optionalGroup.
    def visitOptionalGroup(self, ctx:ASNParser.OptionalGroupContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ASNParser#requiredToken.
    def visitRequiredToken(self, ctx:ASNParser.RequiredTokenContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ASNParser#literal.
    def visitLiteral(self, ctx:ASNParser.LiteralContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ASNParser#primitiveFieldName.
    def visitPrimitiveFieldName(self, ctx:ASNParser.PrimitiveFieldNameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ASNParser#fieldSpec.
    def visitFieldSpec(self, ctx:ASNParser.FieldSpecContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ASNParser#typeFieldSpec.
    def visitTypeFieldSpec(self, ctx:ASNParser.TypeFieldSpecContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ASNParser#typeOptionalitySpec.
    def visitTypeOptionalitySpec(self, ctx:ASNParser.TypeOptionalitySpecContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ASNParser#fixedTypeValueFieldSpec.
    def visitFixedTypeValueFieldSpec(self, ctx:ASNParser.FixedTypeValueFieldSpecContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ASNParser#valueOptionalitySpec.
    def visitValueOptionalitySpec(self, ctx:ASNParser.ValueOptionalitySpecContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ASNParser#variableTypeValueFieldSpec.
    def visitVariableTypeValueFieldSpec(self, ctx:ASNParser.VariableTypeValueFieldSpecContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ASNParser#fixedTypeValueSetFieldSpec.
    def visitFixedTypeValueSetFieldSpec(self, ctx:ASNParser.FixedTypeValueSetFieldSpecContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ASNParser#valueSetOptionalitySpec.
    def visitValueSetOptionalitySpec(self, ctx:ASNParser.ValueSetOptionalitySpecContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ASNParser#object_.
    def visitObject_(self, ctx:ASNParser.Object_Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ASNParser#parameterizedObject.
    def visitParameterizedObject(self, ctx:ASNParser.ParameterizedObjectContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ASNParser#definedObject.
    def visitDefinedObject(self, ctx:ASNParser.DefinedObjectContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ASNParser#objectSet.
    def visitObjectSet(self, ctx:ASNParser.ObjectSetContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ASNParser#objectSetSpec.
    def visitObjectSetSpec(self, ctx:ASNParser.ObjectSetSpecContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ASNParser#fieldName.
    def visitFieldName(self, ctx:ASNParser.FieldNameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ASNParser#valueSet.
    def visitValueSet(self, ctx:ASNParser.ValueSetContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ASNParser#elementSetSpecs.
    def visitElementSetSpecs(self, ctx:ASNParser.ElementSetSpecsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ASNParser#rootElementSetSpec.
    def visitRootElementSetSpec(self, ctx:ASNParser.RootElementSetSpecContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ASNParser#additionalElementSetSpec.
    def visitAdditionalElementSetSpec(self, ctx:ASNParser.AdditionalElementSetSpecContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ASNParser#elementSetSpec.
    def visitElementSetSpec(self, ctx:ASNParser.ElementSetSpecContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ASNParser#unions.
    def visitUnions(self, ctx:ASNParser.UnionsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ASNParser#exclusions.
    def visitExclusions(self, ctx:ASNParser.ExclusionsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ASNParser#intersections.
    def visitIntersections(self, ctx:ASNParser.IntersectionsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ASNParser#unionMark.
    def visitUnionMark(self, ctx:ASNParser.UnionMarkContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ASNParser#intersectionMark.
    def visitIntersectionMark(self, ctx:ASNParser.IntersectionMarkContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ASNParser#elements.
    def visitElements(self, ctx:ASNParser.ElementsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ASNParser#objectSetElements.
    def visitObjectSetElements(self, ctx:ASNParser.ObjectSetElementsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ASNParser#intersectionElements.
    def visitIntersectionElements(self, ctx:ASNParser.IntersectionElementsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ASNParser#subtypeElements.
    def visitSubtypeElements(self, ctx:ASNParser.SubtypeElementsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ASNParser#variableTypeValueSetFieldSpec.
    def visitVariableTypeValueSetFieldSpec(self, ctx:ASNParser.VariableTypeValueSetFieldSpecContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ASNParser#objectFieldSpec.
    def visitObjectFieldSpec(self, ctx:ASNParser.ObjectFieldSpecContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ASNParser#objectOptionalitySpec.
    def visitObjectOptionalitySpec(self, ctx:ASNParser.ObjectOptionalitySpecContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ASNParser#objectSetFieldSpec.
    def visitObjectSetFieldSpec(self, ctx:ASNParser.ObjectSetFieldSpecContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ASNParser#objectSetOptionalitySpec.
    def visitObjectSetOptionalitySpec(self, ctx:ASNParser.ObjectSetOptionalitySpecContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ASNParser#typeAssignment.
    def visitTypeAssignment(self, ctx:ASNParser.TypeAssignmentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ASNParser#valueAssignment.
    def visitValueAssignment(self, ctx:ASNParser.ValueAssignmentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ASNParser#asnType.
    def visitAsnType(self, ctx:ASNParser.AsnTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ASNParser#tag.
    def visitTag(self, ctx:ASNParser.TagContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ASNParser#tagMode.
    def visitTagMode(self, ctx:ASNParser.TagModeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ASNParser#classType.
    def visitClassType(self, ctx:ASNParser.ClassTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ASNParser#builtinType.
    def visitBuiltinType(self, ctx:ASNParser.BuiltinTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ASNParser#objectClassFieldType.
    def visitObjectClassFieldType(self, ctx:ASNParser.ObjectClassFieldTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ASNParser#setType.
    def visitSetType(self, ctx:ASNParser.SetTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ASNParser#setOfType.
    def visitSetOfType(self, ctx:ASNParser.SetOfTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ASNParser#referencedType.
    def visitReferencedType(self, ctx:ASNParser.ReferencedTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ASNParser#definedType.
    def visitDefinedType(self, ctx:ASNParser.DefinedTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ASNParser#constraint.
    def visitConstraint(self, ctx:ASNParser.ConstraintContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ASNParser#constraintSpec.
    def visitConstraintSpec(self, ctx:ASNParser.ConstraintSpecContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ASNParser#userDefinedConstraint.
    def visitUserDefinedConstraint(self, ctx:ASNParser.UserDefinedConstraintContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ASNParser#generalConstraint.
    def visitGeneralConstraint(self, ctx:ASNParser.GeneralConstraintContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ASNParser#userDefinedConstraintParameter.
    def visitUserDefinedConstraintParameter(self, ctx:ASNParser.UserDefinedConstraintParameterContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ASNParser#tableConstraint.
    def visitTableConstraint(self, ctx:ASNParser.TableConstraintContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ASNParser#simpleTableConstraint.
    def visitSimpleTableConstraint(self, ctx:ASNParser.SimpleTableConstraintContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ASNParser#contentsConstraint.
    def visitContentsConstraint(self, ctx:ASNParser.ContentsConstraintContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ASNParser#componentPresenceLists.
    def visitComponentPresenceLists(self, ctx:ASNParser.ComponentPresenceListsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ASNParser#componentPresenceList.
    def visitComponentPresenceList(self, ctx:ASNParser.ComponentPresenceListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ASNParser#componentPresence.
    def visitComponentPresence(self, ctx:ASNParser.ComponentPresenceContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ASNParser#subtypeConstraint.
    def visitSubtypeConstraint(self, ctx:ASNParser.SubtypeConstraintContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ASNParser#value.
    def visitValue(self, ctx:ASNParser.ValueContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ASNParser#builtinValue.
    def visitBuiltinValue(self, ctx:ASNParser.BuiltinValueContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ASNParser#objectIdentifierValue.
    def visitObjectIdentifierValue(self, ctx:ASNParser.ObjectIdentifierValueContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ASNParser#objIdComponentsList.
    def visitObjIdComponentsList(self, ctx:ASNParser.ObjIdComponentsListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ASNParser#objIdComponents.
    def visitObjIdComponents(self, ctx:ASNParser.ObjIdComponentsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ASNParser#integerValue.
    def visitIntegerValue(self, ctx:ASNParser.IntegerValueContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ASNParser#choiceValue.
    def visitChoiceValue(self, ctx:ASNParser.ChoiceValueContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ASNParser#enumeratedValue.
    def visitEnumeratedValue(self, ctx:ASNParser.EnumeratedValueContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ASNParser#signedNumber.
    def visitSignedNumber(self, ctx:ASNParser.SignedNumberContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ASNParser#choiceType.
    def visitChoiceType(self, ctx:ASNParser.ChoiceTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ASNParser#alternativeTypeLists.
    def visitAlternativeTypeLists(self, ctx:ASNParser.AlternativeTypeListsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ASNParser#extensionAdditionAlternatives.
    def visitExtensionAdditionAlternatives(self, ctx:ASNParser.ExtensionAdditionAlternativesContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ASNParser#extensionAdditionAlternativesList.
    def visitExtensionAdditionAlternativesList(self, ctx:ASNParser.ExtensionAdditionAlternativesListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ASNParser#extensionAdditionAlternative.
    def visitExtensionAdditionAlternative(self, ctx:ASNParser.ExtensionAdditionAlternativeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ASNParser#extensionAdditionAlternativesGroup.
    def visitExtensionAdditionAlternativesGroup(self, ctx:ASNParser.ExtensionAdditionAlternativesGroupContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ASNParser#rootAlternativeTypeList.
    def visitRootAlternativeTypeList(self, ctx:ASNParser.RootAlternativeTypeListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ASNParser#alternativeTypeList.
    def visitAlternativeTypeList(self, ctx:ASNParser.AlternativeTypeListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ASNParser#namedType.
    def visitNamedType(self, ctx:ASNParser.NamedTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ASNParser#enumeratedType.
    def visitEnumeratedType(self, ctx:ASNParser.EnumeratedTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ASNParser#enumerations.
    def visitEnumerations(self, ctx:ASNParser.EnumerationsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ASNParser#rootEnumeration.
    def visitRootEnumeration(self, ctx:ASNParser.RootEnumerationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ASNParser#enumeration.
    def visitEnumeration(self, ctx:ASNParser.EnumerationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ASNParser#enumerationItem.
    def visitEnumerationItem(self, ctx:ASNParser.EnumerationItemContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ASNParser#namedNumber.
    def visitNamedNumber(self, ctx:ASNParser.NamedNumberContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ASNParser#definedValue.
    def visitDefinedValue(self, ctx:ASNParser.DefinedValueContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ASNParser#parameterizedValue.
    def visitParameterizedValue(self, ctx:ASNParser.ParameterizedValueContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ASNParser#simpleDefinedValue.
    def visitSimpleDefinedValue(self, ctx:ASNParser.SimpleDefinedValueContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ASNParser#actualParameterList.
    def visitActualParameterList(self, ctx:ASNParser.ActualParameterListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ASNParser#actualParameter.
    def visitActualParameter(self, ctx:ASNParser.ActualParameterContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ASNParser#exceptionSpec.
    def visitExceptionSpec(self, ctx:ASNParser.ExceptionSpecContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ASNParser#exceptionIdentification.
    def visitExceptionIdentification(self, ctx:ASNParser.ExceptionIdentificationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ASNParser#additionalEnumeration.
    def visitAdditionalEnumeration(self, ctx:ASNParser.AdditionalEnumerationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ASNParser#integerType.
    def visitIntegerType(self, ctx:ASNParser.IntegerTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ASNParser#namedNumberList.
    def visitNamedNumberList(self, ctx:ASNParser.NamedNumberListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ASNParser#objectidentifiertype.
    def visitObjectidentifiertype(self, ctx:ASNParser.ObjectidentifiertypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ASNParser#componentRelationConstraint.
    def visitComponentRelationConstraint(self, ctx:ASNParser.ComponentRelationConstraintContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ASNParser#atNotation.
    def visitAtNotation(self, ctx:ASNParser.AtNotationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ASNParser#level.
    def visitLevel(self, ctx:ASNParser.LevelContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ASNParser#componentIdList.
    def visitComponentIdList(self, ctx:ASNParser.ComponentIdListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ASNParser#octetStringType.
    def visitOctetStringType(self, ctx:ASNParser.OctetStringTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ASNParser#bitStringType.
    def visitBitStringType(self, ctx:ASNParser.BitStringTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ASNParser#namedBitList.
    def visitNamedBitList(self, ctx:ASNParser.NamedBitListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ASNParser#namedBit.
    def visitNamedBit(self, ctx:ASNParser.NamedBitContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ASNParser#booleanValue.
    def visitBooleanValue(self, ctx:ASNParser.BooleanValueContext):
        return self.visitChildren(ctx)



del ASNParser