from Mojo.Auth.models import *
from AuthManager import authenticate, login
from uuid import uuid4
import base64, json, datetime

class SessionManager(object):
    def __init__(self, request_handler):
        self.request_handler = request_handler
        self.session_model = None

    def get_or_create_session(self):
        """
        Will get a secure cookie ID from the request OR return an empty session object
        """
        if self.request_handler.get_secure_cookie('session_id'):
            return self.request_handler.get_secure_cookie('session_id'), False
        else:
            new_session = self._create_new_session()
            return new_session, True

    def _logout(self):
        if self.session_model is not None:
            self._set_session_key('logged_in', '')
            logging.debug("Logged out - logged_in key set to: %s", str(self._get_session_key('logged_in')))

        return self.session_model

    def _login(self, userObj):
        if self.session_model is not None:
            self._set_session_key('logged_in', str(userObj._id))

    def _is_logged_in(self):
        if self.session_model is not None:
            if self._get_session_key('logged_in'):
                return self._get_session_key('logged_in')
            else:
                return False
        else:
            return False

    def _log_user_in(self, userObj):
        if self.session_model is not None:
            if self._is_session_valid():
                self._set_session_key('logged_in', str(userObj._id))
            else:
                #TODO: These should raise errors
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
        session_data = self._decode_session(self.session_model.session_data.get_value())
        session_data[key] = value
        enc_data = self._encode_session(session_data)
        self.session_model.session_data = enc_data

    def _get_session_key(self, key):
        #TODO: It's not saving session data AT ALL
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
        new_session = Session()._setup_session()
        self.session_model = new_session
        self.request_handler.set_secure_cookie('session_id', new_key)
        return self.session_model

def Setup_session(sessionObj, expiry_days=30, expiry_hours=0, expiry_minutes=0):
    sessionObj.session_key = str(uuid.uuid4())
    expiry_date = datetime.datetime.now() +datetime.timedelta(days=expiry_days, hours=expiry_hours, minutes = expiry_minutes)
    sessionObj.session_expires = expiry_date

    return sessionObj

def Reset_session(sessionObj, expiry_days=30, expiry_hours=0, expiry_minutes=0):
    expiry_date = datetime.datetime.now() +datetime.timedelta(days=expiry_days, hours=expiry_hours, minutes = expiry_minutes)
    sessionObj.session_expires = expiry_date

    return sessionObj