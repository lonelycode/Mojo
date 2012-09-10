from Mojo.ObjectMapper.ModelPrototype import Model, EmbeddedModelField
from Mojo.ObjectMapper.Fields import *
import uuid, datetime

class Profile(Model):
    _id = ObjectIDField()
    first_name = StringField()
    last_name = StringField()


class Group(Model):
    _id = ObjectIDField()
    group_name = StringField(allow_empty=False)

class User(Model):
    _id = ObjectIDField()
    username = StringField(allow_empty=False)
    password = StringField(allow_empty=False)
    email = StringField()
    groups = ListField()
    active = BooleanField(default = True)
    profile = EmbeddedModelField(to=Profile)
    is_superuser = BooleanField(default = False)
    last_login = DateTimeField()
    date_joined = DateTimeField()

class Session(Model):
    _id = ObjectIDField()
    session_key = StringField(allow_empty=False)
    session_data = StringField()
    session_expires = DateTimeField()