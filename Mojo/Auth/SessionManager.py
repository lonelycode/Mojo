from Mojo.Auth.models import *
from AuthManager import authenticate, login
from uuid import uuid4
import base64, json, datetime

class SessionManager(object):
    def __init__(self, request_handler):
        self.request_handler = request_handler
        self.session_model = None
        self.session_id = None
        self.cookies = self.get_session_cookies()

    def get_session_cookies(self):
        """
        Will get a secure cookie ID from the request OR return an empty session object
        """

        cookies = {}
        if self.request_handler.get_secure_cookie('session_id'):
            cookies['session_id'] = self.request_handler.get_secure_cookie('session_id')
            self.session_id = cookies['session_id']

        if self.request_handler.get_secure_cookie('logged_in'):
            cookies['logged_in'] = self.request_handler.get_secure_cookie('logged_in')

        return cookies

    def _logout(self):
        self.request_handler.set_secure_cookie('logged_in', '')
        return True

    def _login(self, userObj):
        self.request_handler.set_secure_cookie('logged_in', str(userObj._id))
        return True

    def _is_logged_in(self):
        if 'logged_in' in self.get_session_cookies().keys():
            cookies = self.get_session_cookies()
            if cookies['logged_in'] is not None:
                return True
            else:
                return False
        else:
            return False

    def _is_session_valid(self):
        if self.session_model is not None:
            if self.session_model.session_expires.get_value() > datetime.datetime.now():
                return True
            else:
                return False
        else:
            return False

    def _set_session_key(self, key, value):
        if self.session_model.session_data is not None:
            session_data = self._decode_session(self.session_model.session_data.get_value())
            session_data[key] = value
        else:
            session_data = {key:value}

        enc_data = self._encode_session(session_data)
        self.session_model.session_data = enc_data

    def _get_session_key(self, key):
        if self._is_session_valid():
            session_data = {}
            if self.session_model is not None:
                session_data = self._decode_session(self.session_model.session_data.get_value())

            if key in session_data:
                return session_data[key]
            else:
                return None
        else:
            return None

    def _decode_session(self, session_data):
        if session_data is not None:

            jsonStr = base64.b64decode(session_data)
            session_dict = json.loads(jsonStr)

            return session_dict
        else:
            return {}

    def _encode_session(self, session_data):
        session_json_str = json.dumps(session_data)
        encoded_str = base64.b64encode(session_json_str)

        return encoded_str

    def _create_new_session(self):
        new_key = str(uuid4())
        new_session = Setup_session(Session())
        self.session_model = new_session
        self.request_handler.set_secure_cookie('session_id', new_key)
        return self.session_model

def Setup_session(sessionObj, expiry_days=30, expiry_hours=0, expiry_minutes=0):
    sessionObj.session_key = str(uuid.uuid4())
    expiry_date = datetime.datetime.now() +datetime.timedelta(days=expiry_days, hours=expiry_hours, minutes = expiry_minutes)
    sessionObj.session_expires = expiry_date
    sessionObj.session_data = {}

    return sessionObj

def Reset_session(sessionObj, expiry_days=30, expiry_hours=0, expiry_minutes=0):
    expiry_date = datetime.datetime.now() +datetime.timedelta(days=expiry_days, hours=expiry_hours, minutes = expiry_minutes)
    sessionObj.session_expires = expiry_date

    return sessionObj