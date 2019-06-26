# Auto generated from tests\test_pyjsg_standalone\test_jsg_readme\jsg\type_directive_1.jsg by PyJSG version 0.9.1
# Generation date: 2019-06-26 14:26
#
import typing
import pyjsg.jsglib as jsg

# .TYPE and .IGNORE settings
_CONTEXT = jsg.JSGContext()
_CONTEXT.TYPE_EXCEPTIONS.append("doc")


class doc(jsg.JSGObject):
    _reference_types = []
    _members = {'a': jsg.AnyTypeFactory('a', _CONTEXT)}
    _strict = True

    def __init__(self,
                 a: object = jsg.Empty,
                 **_kwargs: typing.Dict[str, object]):
        super().__init__(_CONTEXT, **_kwargs)
        self.a = a


_CONTEXT.NAMESPACE = locals()
