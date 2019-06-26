
import unittest
from typing import cast

from pyjsg.parser_impl.jsg_arrayexpr_parser import JSGArrayExpr
from tests.test_pyjsg.test_basics.parser import parse


class ArrayExprTestCase(unittest.TestCase):
    def check(self, t: JSGArrayExpr, expected) -> None:
        tup = (str(t), t.python_type(), t.dependency_list(), t.signature_type(), t.mt_value(), t.members_entries())
        self.assertEqual(expected, tup)

    def test_basics(self):
        t = cast(JSGArrayExpr, parse("id [@string] ", "arrayDef", JSGArrayExpr))
        self.check(t,
              ('arrayExpr: [valueType: builtinValueType: @string]',
               'typing.List[str]',
                [],
                "jsg.ArrayFactory('{name}', _CONTEXT, jsg.String, 0, None)",
                'None',
                []))

        t = cast(JSGArrayExpr, parse("id [@int] ", "arrayDef", JSGArrayExpr))
        self.check(t,
              ('arrayExpr: [valueType: builtinValueType: @int]',
               'typing.List[int]',
               [],
               "jsg.ArrayFactory('{name}', _CONTEXT, jsg.Integer, 0, None)",
               'None',
               [])
              )

        t = cast(JSGArrayExpr, parse("id [.] ", "arrayDef", JSGArrayExpr))
        self.check(t,
              ('arrayExpr: [valueType: builtinValueType: jsg.AnyType]',
               'typing.List[object]',
               [],
               "jsg.ArrayFactory('{name}', _CONTEXT, jsg.AnyTypeFactory('{name}', _CONTEXT), 0, None)",
               'None',
               [])
              )

        t = cast(JSGArrayExpr, parse("id [(Aa|BB|'foo')] ", "arrayDef", JSGArrayExpr))
        self.check(t,
              ("arrayExpr: [valueType: ((STRING: pattern: r'foo') | Undefined(Aa) | BB)]",
               'typing.List[typing.Union[str, Undefined(Aa), str]]',
               ['_Anon1', 'Aa', 'BB'],
               "jsg.ArrayFactory('{name}', _CONTEXT, typing.Union[_Anon1, Undefined(Aa), BB], 0, None)",
               'None',
               [])
              )

        t = cast(JSGArrayExpr, parse("id [(Aa|BB|'foo'){0,}] ", "arrayDef", JSGArrayExpr))
        self.check(t,
              ("arrayExpr: [valueType: ((STRING: pattern: r'foo') | Undefined(Aa) | BB){0,}]",
                'typing.List[typing.Union[str, Undefined(Aa), str]]',
               ['_Anon1', 'Aa', 'BB'],
               "jsg.ArrayFactory('{name}', _CONTEXT, typing.Union[_Anon1, Undefined(Aa), BB], 0, None)",
               'None',
               [])
              )

    def test_options(self):
        txt = "exclusions [(objectValue|LanguageStem) +]"
        t = cast(JSGArrayExpr, parse(txt, "arrayDef", JSGArrayExpr))
        self.check(t,
                   ('arrayExpr: [valueType: (Undefined(objectValue) | Undefined(LanguageStem))+]',
                    'typing.List[typing.Union[Undefined(objectValue), Undefined(LanguageStem)]]',
                    ['objectValue', 'LanguageStem'],
                    "jsg.ArrayFactory('{name}', _CONTEXT, typing.Union[Undefined(objectValue), Undefined(LanguageStem)], 1, None)",
                    'None',
                    [])
                   )

    def test_multi_types(self):
        txt = "x [objectValue | languageStem {3,7}]"
        t = cast(JSGArrayExpr, parse(txt, "arrayDef", JSGArrayExpr))
        self.check(t,
                   ('arrayExpr: [(valueType: ID: objectValue | valueType: ID: '
                    'languageStem){3,7}]',
                    'typing.List[typing.Union[Undefined(objectValue), Undefined(languageStem)]]',
                    ['objectValue', 'languageStem'],
                    "jsg.ArrayFactory('{name}', _CONTEXT, typing.Union[Undefined(objectValue), Undefined(languageStem)], 3, 7)",
                    'None',
                    [])
                   )


if __name__ == '__main__':
    unittest.main()

