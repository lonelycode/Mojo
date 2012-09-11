import logging
from Mojo.Auth.SessionManager import SessionManager
from Mojo.Auth.AuthManager import authenticate

def login_assistant(thisUser, password, request):
    logging.debug('Found user: %s' % thisUser)

    if thisUser is not None:
        # We now have a user, let's authenticate her
        is_authenticated = authenticate(thisUser, password)
        logging.debug('Checking is user is authenticated: %s' % str(is_authenticated))
        if is_authenticated:
            SessionManager(request)._login(thisUser)
            return True
        else:
            return False
    else:
        return False

def logout_assistant(request):
    SessionManager(request)._logout()
    return True