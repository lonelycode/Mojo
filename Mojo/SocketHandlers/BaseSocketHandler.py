from tornadio2 import SocketConnection
import logging

CURRENT_SESSIONS = {}
LOGGED_IN_SESSIONS = {}

class MojoSocketHandler(SocketConnection):
    """
    The ``MojoSocketHandler`` overrides the ``on_open`` and ``on_close`` events of the standard ``TornadIO2`` ``SocketConnection``
    to expose some simple session data (``self.session_id`` and ``self.logged_in``).

    ``MojoSocketHandler`` will store connections in a global dictionary called ``CURRENT_SESSIONS``, all connections are keyed
    by the user ``session_id`` (generated automatically on request).

    You can import ``CURRENT_SESSIONS`` to broadcast to all users, or emit messages to specific users based on their
    ``session_id``.

    If you are using the ``Mojo.Auth`` module, and the cookie ``logged_in`` is set (i.e. the user is logged in), then another
    global dictionary: ``LOGGED_IN_SESSIONS`` is populated with the connection, keyed by the ``user_id`` of the user. This makes
    common tasks much simpler to manage such as:

    - Broadcasting to all connected clients
    - Broadcasting to only logged in users
    - Online 'status' checking of logged in users - e.g. for chat.
    - Event-based messaging, e.g. with signals

    """

    def on_open(self, request):
        from settings import COOKIE_SECRET
        from tornado.web import decode_signed_value

        self.session_id = None
        self.logged_in = None

        if 'session_id' in request.cookies:
            self.session_id = decode_signed_value(COOKIE_SECRET, 'session_id', unicode(request.get_cookie('session_id').value))

            global CURRENT_SESSIONS
            CURRENT_SESSIONS[self.session_id] = self

        if 'logged_in' in request.cookies:
            val = decode_signed_value(COOKIE_SECRET, 'logged_in', unicode(request.get_cookie('logged_in').value))
            if val != '':
                self.logged_in = val

            if self.logged_in is not None:
                global LOGGED_IN_SESSIONS
                LOGGED_IN_SESSIONS[self.logged_in] = self



    def on_close(self):
        global CURRENT_SESSIONS
        global LOGGED_IN_SESSIONS

        for key in CURRENT_SESSIONS:
            if CURRENT_SESSIONS[key] == self:
                del CURRENT_SESSIONS[key]
                break

        for key in LOGGED_IN_SESSIONS:
            if LOGGED_IN_SESSIONS[key] == self:
                del LOGGED_IN_SESSIONS[key]
                break

    def on_message(self, msg):
        pass