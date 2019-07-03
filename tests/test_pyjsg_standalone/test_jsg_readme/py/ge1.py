# Auto generated from tests\test_pyjsg_standalone\test_jsg_readme\jsg\ge1.jsg by PyJSG version 0.9.2
# Generation date: 2019-07-03 17:39
#
import typing
import pyjsg.jsglib as jsg

# .TYPE and .IGNORE settings
_CONTEXT = jsg.JSGContext()
_CONTEXT.TYPE = "type"
_CONTEXT.TYPE_EXCEPTIONS.append("person")


class _Anon1(jsg.JSGString):
    pattern = jsg.JSGPattern(r'(m)|(f)')


class details(jsg.JSGObject):
    _reference_types = []
    _members = {'id': jsg.String}
    _strict = False

    def __init__(self,
                 id: str = None,
                 **_kwargs: typing.Dict[str, object]):
        super().__init__(_CONTEXT, **_kwargs)
        self.id = id



class person(jsg.JSGObject):
    _reference_types = [details]
    _members = {'name': jsg.String,
                'gender': _Anon1,
                'active': jsg.Boolean,
                'id': jsg.ArrayFactory('id', _CONTEXT, jsg.String, 0, None)}
    _strict = True

    def __init__(self,
                 name: str = None,
                 gender: str = None,
                 active: bool = None,
                 id: str = None,
                 **_kwargs: typing.Dict[str, object]):
        super().__init__(_CONTEXT, **_kwargs)
        self.name = name
        self.gender = gender
        self.active = active
        self.id = id



class company(jsg.JSGObject):
    _reference_types = []
    _members = {'name': jsg.String,
                'year founded': typing.Optional[jsg.Integer],
                'employees': jsg.ArrayFactory('employees', _CONTEXT, person, 2, None)}
    _strict = True

    def __init__(self,
                 name: str = None,
                 employees: typing.List[person] = None,
                 **_kwargs: typing.Dict[str, object]):
        super().__init__(_CONTEXT, **_kwargs)
        self.name = name
        setattr(self, 'year founded', _kwargs.get('year founded', None))
        self.employees = employees


_CONTEXT.NAMESPACE = locals()
