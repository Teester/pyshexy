# Auto generated from tests\test_pyjsg\test_basics\jsg\simplelexer.jsg by PyJSG version 0.9.1
# Generation date: 2019-06-26 14:26
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
    pattern = jsg.JSGPattern(r'@[a-zA-Z]+(\-[a-zA-Z0-9]+)*')

_CONTEXT.NAMESPACE = locals()
