from Mojo.ObjectMapper.ModelPrototype import Model, EmbeddedModelField
from Mojo.ObjectMapper.Fields import *
import uuid, datetime

class Profile(Model):
    """
    Represents a user profile - currently cannot be extended. Is an embedded document in a ``User`` object.
    """
    _id = ObjectIDField()
    first_name = StringField()
    last_name = StringField()


class Group(Model):
    """
    Group definition - consists only of the name of the group, is part of a ``ListField`` in the ``User`` object
    """
    _id = ObjectIDField()
    group_name = StringField(allow_empty=False)

class User(Model):
    """
    Main User model used by the ``Mojo.Auth`` modules, consists of multiple fields:

    - ``username``: The username of the user (required)
    - ``password``: The ``bcrypt`` encrypted password (required)
    - ``email``: the email address of the user (optional)
    - ``groups``: A list field of ``Group`` objects that the user belongs to
    - ``active``: Is the user active, and allowed in?
    - ``profile``: An embedded field that uses the ``Profile`` model
    - ``is_superuser``: Flag to indicate super user status (``BooleanField``)
    - ``last_login``: ``DateTimeField`` with last login date/time
    - ``date_joined``: Can be set to when the user joined (``DateTimeField``)

    """

    _id = ObjectIDField()
    username = StringField(allow_empty=False)
    password = StringField(allow_empty=False)
    email = StringField()
    groups = ListField(of=Group)
    active = BooleanField(default = True)
    profile = EmbeddedModelField(to=Profile)
    is_superuser = BooleanField(default = False)
    last_login = DateTimeField()
    date_joined = DateTimeField()

class Session(Model):
    """
    The ``Session`` object is mainly used as part of the ``SessionManager`` class and the ``SessionMixin`` mix-in base class.

    This should **not** be manipulated directly, but stores any session information in the ``session_data`` database field.

    Data stored in ``session_data`` is a JSON string that is base64 encoded, user log in flags are *not* stored in ``session_data`` to
    avoid hitting the database every time ``current_user`` is queried in a request.
    """
    _id = ObjectIDField()
    session_key = StringField(allow_empty=False)
    session_data = StringField()
    session_expires = DateTimeField()