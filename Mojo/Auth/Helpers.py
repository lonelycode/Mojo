import logging
from Mojo.Auth.SessionManager import SessionManager
from Mojo.Auth.AuthManager import authenticate

def login_assistant(thisUser, password, request):
    """
    Shortcut function that will perform three things at once:

    #. Checks if the user exists
    #. Authenticates the user against a password using ``Auth.AuthManager.authenticate()``
    #. If authenticated, sets the appropriate session cookie (that is checked by ``get_current_user()`` and returns ``True``

    **Parameters**

    - ``thisUser`` - Mojo.Auth.models.User object
    - ``password`` - string password representation
    - ``request`` - RequestHandler object, does *not* require the Session Mixin to be used.

    **Usage:** ::

        from Mojo.Auth.Helpers import login_assitant

        thisUser = Users.find_one({'_id':ObjectId('504e0439a9ee2f04a0835a92'})

        if thisUser:
            is_authenticated = login_assistant(thisUser, password, self) #self in this case is a RequestHandler
            if is_authenticated:
                ...
            else:
                ...

    """
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
    """
    Shortcut function to log a user out. Uses ``Mojo.Auth.SessionManager`` to set the appropriate
    session cookie and returns ``True``.

    Once called, ``get_current_user()`` and ``curent_user`` will be returned as ``None`` in a RequestHandler.

    """
    SessionManager(request)._logout()
    return True