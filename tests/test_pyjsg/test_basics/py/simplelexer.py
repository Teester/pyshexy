# Auto generated from tests\test_pyjsg\test_basics\jsg\simplelexer.jsg by PyJSG version 0.9.2
# Generation date: 2019-07-03 17:37
#
import typing
import pyjsg.jsglib as jsg

# .TYPE and .IGNORE settings
_CONTEXT = jsg.JSGContext()



class HEX(jsg.JSGString):
    pattern = jsg.JSGPattern(r'[0-9]|[A-F]|[a-f]')


class EXPONENT(jsg.JSGString):
    pattern = jsg.JSGPattern(r'[eE][+-]?[0-9]+')


class LANGTAG(jsg.JSGString):
    pattern = jsg.JSGPattern(r'\@[a-zA-Z]+(\-[a-zA-Z0-9]+)*')

_CONTEXT.NAMESPACE = locals()
