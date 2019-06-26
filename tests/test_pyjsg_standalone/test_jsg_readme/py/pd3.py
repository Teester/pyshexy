# Auto generated from tests\test_pyjsg_standalone\test_jsg_readme\jsg\pd3.jsg by PyJSG version 0.9.1
# Generation date: 2019-06-26 14:26
#
import typing
import pyjsg.jsglib as jsg

# .TYPE and .IGNORE settings
_CONTEXT = jsg.JSGContext()
_CONTEXT.TYPE = "id"
_CONTEXT.TYPE_EXCEPTIONS.append("person")
_CONTEXT.IGNORE.append("height")
_CONTEXT.IGNORE.append("weight")
_CONTEXT.IGNORE.append("location")


class person(jsg.JSGObject):
    _reference_types = []
    _members = {'name': jsg.String,
                'age': jsg.Integer}
    _strict = True

    def __init__(self,
                 name: str = None,
                 age: int = None,
                 **_kwargs: typing.Dict[str, object]):
        super().__init__(_CONTEXT, **_kwargs)
        self.name = name
        self.age = age



class membership(jsg.JSGObject):
    _reference_types = []
    _members = {'list_name': jsg.String,
                'members': jsg.ArrayFactory('members', _CONTEXT, person, 0, None)}
    _strict = True

    def __init__(self,
                 list_name: str = None,
                 members: typing.List[person] = None,
                 **_kwargs: typing.Dict[str, object]):
        super().__init__(_CONTEXT, **_kwargs)
        self.list_name = list_name
        self.members = members


_CONTEXT.NAMESPACE = locals()
