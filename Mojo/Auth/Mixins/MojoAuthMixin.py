from tornado.web import RequestHandler
import logging
from tornado import gen

class MojoAuthMixin(RequestHandler):
    def get_current_user(self):
        if self.application.mojo_settings.USE_AUTH:

            logging.debug('get_current_user called, not cached!')
            from Mojo.Auth.SessionManager import SessionManager

            if hasattr(self, 'session'):
                SM = self.session
            else:
                SM = SessionManager(self)
                self.session = SM

            if not SM._is_logged_in():
                logging.debug('Session is created... no user to report')
                return None
            else:
                return SM.cookies['logged_in']

        else:
            logging.warning('Mojo Auth module not implemented, please override get_current_user or implement Auth module.')