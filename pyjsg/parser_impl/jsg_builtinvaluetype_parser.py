# from dataclasses import dataclass
from typing import Optional, Tuple, Dict, List

from pyjsg.parser.jsgParser import *
from pyjsg.parser.jsgParserVisitor import jsgParserVisitor
from pyjsg.parser_impl.jsg_doc_context import JSGDocContext, PythonGeneratorElement

        
class JSGBuiltinValueType(jsgParserVisitor, PythonGeneratorElement):
    # @dataclass
    class TypeInfo:
        def __init__(self, sig_type: str, ref_type: str, py_type: type, mt_value: str):
            self.sig_type = sig_type
            self.ref_type = ref_type
            self.py_type = py_type
            self.mt_value = mt_value
            
        def __repr__(self):
            return "{}(sig_type={}!r, ref_type={}!r, py_type={}!r, mt_value={}!r)".format(self.__class__.__name__,
                                                                                          self.sig_type,
                                                                                          self.ref_type,
                                                                                          self.py_type,
                                                                                          self.mt_value)

        def __eq__(self, other):
            if other.__class__ is not self.__class__:
                return NotImplemented
            return (self.sig_type, self.ref_type, self.py_type, self.mt_value) == (other.sig_type,
                                                                                   other.ref_type,
                                                                                   other.py_type,
                                                                                   other.mt_value)

    parserTypeToImplClass = \
        {"@string": TypeInfo("jsg.String", "jsg.String", str, "None"),
         "@object": TypeInfo("jsg.ObjectFactory('{name}', _CONTEXT, jsg.Object)", "jsg.JSGObject", object, "None"),
         "@int": TypeInfo("jsg.Integer", "jsg.Integer", int, "None"),
         "@number": TypeInfo("jsg.Number", "jsg.Number", float, "None"),
         "@null": TypeInfo("jsg.JSGNull", "jsg.JSGNull", type(None), "jsg.Empty"),
         "@array": TypeInfo("jsg.ArrayFactory('{name}', _CONTEXT, jsg.AnyType, 0, None)", "jsg.JSGArray", list, "None"),
         "@bool": TypeInfo("jsg.Boolean", "jsg.Boolean", bool, "None"),
         ".": TypeInfo("jsg.AnyTypeFactory('{name}', _CONTEXT)", "jsg.AnyType", object, "jsg.Empty")}

    def __init__(self, context: JSGDocContext, ctx: Optional[jsgParser.BuiltinValueTypeContext] = None):
        self._context = context
        self._value_type_text = None  # type: Optional[str]
        self._typeinfo = None  # type: JSGBuiltinValueType.TypeInfo
        self.text = ""
        if ctx:
            self.text = ctx.getText()
            self.visit(ctx)

    def __str__(self):
        return "builtinValueType: {}".format(self._value_type_text if self._value_type_text != '.' else 'jsg.AnyType')

    def python_type(self) -> str:
        return "type(None)" if self._typeinfo.py_type is type(None) else self._typeinfo.py_type.__name__

    def signature_type(self) -> str:
        return self._typeinfo.sig_type

    def reference_type(self) -> str:
        return self._typeinfo.sig_type

    def mt_value(self) -> str:
        return self._typeinfo.mt_value

    def members_entries(self, all_are_optional: Optional[bool] = False) -> List[Tuple[str, str]]:
        return []

    def dependency_list(self) -> List[str]:
        return []

    # ***************
    #   Visitors
    # ***************
    def visitBuiltinValueType(self, ctx: jsgParser.BuiltinValueTypeContext):
        """ valueTypeExpr: JSON_STRING | JSON_NUMBER | JSON_INT | JSON_BOOL | JSON_NULL | JSON_ARRAY | JSON_OBJECT """
        self._value_type_text = ctx.getText()
        self._typeinfo = self.parserTypeToImplClass[self._value_type_text]
