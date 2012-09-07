from Mojo.Auth.models import *
from AuthManager import authenticate, login
from uuid import uuid4
import base64, json, datetime

class SessionManager(object):
    def __init__(self, request_handler):
        self.request_handler = request_handler
        self.session_model = None

    def get_or_create_session(self):
        if self.request_handler.get_secure_cookie('session_id'):
            return self.request_handler.get_secure_cookie('session_id'), False
        else:
            new_session = self._create_new_session()
            return new_session, True

    def _logout(self):
        if self.session_model:
            self._set_session_key('logged_in', False)

        return self.session_model

    def _login(self):
        if self.session_model:
            self._set_session_key('logged_in', True)

    def _is_logged_in(self):
        if self.session_model:
            if self._get_session_key('logged_in'):
                return self._get_session_key('logged_in')
            else:
                return False
        else:
            return False

    def _is_session_valid(self):
        if self.session_model:
            if self.session_model.session_expires > datetime.datetime.now():
                return True
            else:
                return False
        else:
            return False

    def _set_session_key(self, key, value):
        session_data = self._decode_session(self.session_model.session_data)
        session_data[key] = value
        enc_data = self._encode_session(session_data)
        self.session_model.session_data = enc_data

    def _get_session_key(self, key):
        session_data = self._decode_session(self.session_model.session_data)
        if key in session_data:
            return session_data[key]
        else:
            return False

    def _decode_session(self, session_data):
        jsonStr = base64.b64decode(session_data)
        session_dict = json.loads(jsonStr)

        return session_dict

    def _encode_session(self, session_data):
        session_json_str = json.dumps(session_data)
        encoded_str = base64.b64encode(session_json_str)

        return encoded_str

    def _create_new_session(self):
        new_key = str(uuid4())
        new_session = Session()._setup_session()
        self.request_handler.set_secure_cookie('session_id', new_key)
        return new_session