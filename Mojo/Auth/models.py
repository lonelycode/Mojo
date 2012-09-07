from Mojo.ObjectMapper.ModelPrototype import Model, EmbeddedModelField
from Mojo.ObjectMapper.Fields import *
import uuid, datetime

class Profile(Model):
    _id = StringField()
    first_name = StringField()
    last_name = StringField()


class Group(Model):
    _id = StringField()
    group_name = StringField(allow_empty=False)

class User(Model):
    _id = StringField()
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
    _id = StringField()
    session_key = StringField(allow_empty=False)
    session_data = StringField()
    session_expires = DateTimeField()

    def _setup_session(self, expiry_days=30, expiry_hours=0, expiry_minutes=0):
        self.session_key = str(uuid.uuid4())
        expiry_date = datetime.datetime.now() +datetime.timedelta(days=expiry_days, hours=expiry_hours, minutes = expiry_minutes)
        self.session_expires = expiry_date