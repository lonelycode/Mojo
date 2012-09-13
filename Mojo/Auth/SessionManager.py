from Mojo.Auth.models import *
from AuthManager import authenticate, login
from uuid import uuid4
import base64, json, datetime

class SessionManager(object):
    """
    ``SessionManager`` is meant to make it easier to manage sesison cookies and persistent session data by providing a series of
    methods that can be used to log a user in, log a user out, get all cookie data.

    The ``SessionManager`` also manages the encoding, decoding, getting and setting of persistent session data and session valididty,
    it can be used on it's own or through the ``SessionMixin`` base class.

    For example, the ``Mojo.Auth.Helpers.login_assitant`` function will use a ``SessionManager`` class to get and set the cookies
    that log a uder in and out, while the ``SessionMixin`` class will also get and set persistent session data and save it to
    the database automatically, making sesison manageent easier and more secure.

    ``SessionManager`` objects take a ``RequestHandler`` as an init parameter in order to function::

        if thisUser is not None:
            if is_authenticated:
                SessionManager(request)._login(thisUser) #Will make the relevant changes to the cookies.
                return True
            else:
                return False
        else:
            return False

    """
    def __init__(self, request_handler):
        self.request_handler = request_handler
        self.session_model = None
        self.session_id = None
        self.cookies = self.get_session_cookies()

    def get_session_cookies(self):
        """
        Returns Mojo-specific cookie data:

        - ``session_id`` - the ID used to lookup the session in the database
        - ``logged_in`` - the _id of the User model that is currently logged in

        Cookie data is returned as a ``dict``
        """

        cookies = {}
        if self.request_handler.get_secure_cookie('session_id'):
            cookies['session_id'] = self.request_handler.get_secure_cookie('session_id')
            self.session_id = cookies['session_id']

        if self.request_handler.get_secure_cookie('logged_in'):
            cookies['logged_in'] = self.request_handler.get_secure_cookie('logged_in')

        return cookies

    def _logout(self):
        '''
        Set the secure cookie to log a user out - essentially setting the ``logged_in`` session cookie to blank.
        '''
        self.request_handler.set_secure_cookie('logged_in', '')
        return True

    def _login(self, userObj):
        '''
        Set the secure cookie to log a user in, the valud of ``logged_in`` is set to the ``_id`` of the User object.
        '''
        self.request_handler.set_secure_cookie('logged_in', str(userObj._id))
        return True

    def _is_logged_in(self):
        '''
        Checks if a user is logged in, will get the session cookies and check the ``logged_in`` value to see if it is None
        returns ``True`` or ``False depending on the outcome.
        '''
        if 'logged_in' in self.get_session_cookies().keys():
            cookies = self.get_session_cookies()
            if cookies['logged_in'] is not None:
                return True
            else:
                return False
        else:
            return False

    def _is_session_valid(self):
        '''
        This queries the session model in the database to check if the session has expired or not - this is *not* the same
        as the cookie expiry. Returns ``True`` or ``False``
        '''
        if self.session_model is not None:
            if self.session_model.session_expires.get_value() > datetime.datetime.now():
                return True
            else:
                return False
        else:
            return False

    def _set_session_key(self, key, value):
        '''
        Sets a session key to be stored in the session model. Session data is stored as a base64-encoded ``JSON`` string, and so the
        function will go through a `check -> decode -> set` process and set the ``session_model`` attribute of the ``SesionManager``
        '''
        if self.session_model.session_data is not None:
            session_data = self._decode_session(self.session_model.session_data.get_value())
            session_data[key] = value
        else:
            session_data = {key:value}

        enc_data = self._encode_session(session_data)
        self.session_model.session_data = enc_data

    def _get_session_key(self, key):
        '''
        Gets a session value stored in the session model by it's key. Session data is stored as a base64-encoded ``JSON`` string, and so the
        function will go through a `check -> decode -> set -> encode -> return` process and get the ``key`` value of the ``session_data``
        of the ``session_model`` attribute.
        '''
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
        '''
        Internal helper function that decodes the ``session_data`` attribute of the ``session_model``.
        '''
        if session_data is not None:

            jsonStr = base64.b64decode(session_data)
            session_dict = json.loads(jsonStr)

            return session_dict
        else:
            return {}

    def _encode_session(self, session_data):
        '''
        Internal helper function that encodes the ``session_data`` attribute of the ``session_model``.
        '''
        session_json_str = json.dumps(session_data)
        encoded_str = base64.b64encode(session_json_str)

        return encoded_str

    def _create_new_session(self):
        '''
        Creates and sets up a new ``session_model`` ready for the request.
        '''
        new_session = Setup_session(Session())
        self.session_model = new_session
        self.request_handler.set_secure_cookie('session_id', new_session.session_key.get_value())
        return self.session_model

def Setup_session(sessionObj, expiry_days=30, expiry_hours=0, expiry_minutes=0):
    '''
    Helper function that will take a ''session_model'' object and apply the base data to it ready for use in a
    ''RequestHandler'' or ''SessionManager''. By default, a session will expire after 30 days.

    **Paramaters**:

    - ``sessionObj`` - The session_model to be initialised
    - ``expiry_days`` - How long the session shoul last (optional, default is 30 days)
    - ``expiry_hours`` - How long the session should last i hours (optional)
    - ``expiry_minutes`` - How long the session should last in minutes (optional)

    **Usage:** ::

        from Auth.SessionManager import Setup_session
        from Auth.models import Session

        new_session = Setup_session(Session())

    '''
    sessionObj.session_key = str(uuid.uuid4())
    expiry_date = datetime.datetime.now() +datetime.timedelta(days=expiry_days, hours=expiry_hours, minutes = expiry_minutes)
    sessionObj.session_expires = expiry_date
    sessionObj.session_data = {}

    return sessionObj

def Reset_session(sessionObj, expiry_days=30, expiry_hours=0, expiry_minutes=0):
    '''
    Resets an exisitng session - for example, if a user has logged in again, the expiry date needs to be extended to another 30 days.
    Takes the same parameters as ``Setup_session()``:

    **Paramaters**:

    - ``sessionObj`` - The session_model to be initialised
    - ``expiry_days`` - How long the session shoul last (optional, default is 30 days)
    - ``expiry_hours`` - How long the session should last i hours (optional)
    - ``expiry_minutes`` - How long the session should last in minutes (optional)

    '''
    expiry_date = datetime.datetime.now() +datetime.timedelta(days=expiry_days, hours=expiry_hours, minutes = expiry_minutes)
    sessionObj.session_expires = expiry_date

    return sessionObj