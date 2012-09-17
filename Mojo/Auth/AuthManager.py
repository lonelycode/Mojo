import bcrypt, string, random, datetime

def authenticate(userObj, password):
    """
    Will check if a user password matches the input to authenticate the user,
    this will **not** log them in::

        from Mojo.Auth.AuthManager import authenticate

        thisUser = Users.find_one({'_id':ObjectId('504e0439a9ee2f04a0835a92'})
        authenticated = authenticate(thisUser, password)
        if authenticated:
            #Process the login
            ...
        else:
            ...

    Will return ``True`` if passwords matches and ``False`` if password doesn't match.

    Authentication in Mojo uses the ``bcrypt`` library for encrypting passwords and is a requirement for using
    the Auth module.
    """
    if bcrypt.hashpw(password, userObj.password) == userObj.password:
        return True
    else:
        return False

def set_password(userObj, new_password):
    """
    Sets the user password and returns the user object, *the object is not saved to the database*.
    Usage requires ``bcrypt`` to be installed alongside Mojo::

        from Mojo.Auth.AuthManager import set_password

        thisUser = Users.find_one({'_id':ObjectId('504e0439a9ee2f04a0835a92'})
        thisUser = set_password(thisUser, 'new-password=string')
        thisUser.save() #save the user object to the database.

    """
    new_pw = bcrypt.hashpw(new_password, bcrypt.gensalt())
    userObj.password = new_pw

    return userObj

def make_random_password():
    """
    Generates a random string consisting of 8 characters chosen from the uppercase ascii alphabet
    and digits.

    Returns string.
    """

    return ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(8))

def login(userObj):
    """
    If you are using the Auth module and want to track login times as part of the userObj, use this
    to set the appropriate state of the user objects last_login field, can be used in conjunction with
    ``Mojo.Auth.Helpers.login_assistant()`` to round-off the login process::

        from Mojo.Auth.AuthManager import login
        from Mojo.Auth.Helpers import login_assitant

        thisUser = Users.find_one({'_id':ObjectId('504e0439a9ee2f04a0835a92'})

        if thisUser:
            is_authenticated = login_assistant(thisUser, password, self) #self in this case is a RequestHandler
            if is_authenticated:
                login(thisUser)             #set the last_login
                thisUser.save()             #save the user
            else:
                ...


    """
    userObj.last_login = datetime.datetime.now()

    return userObj

def is_member_of(userObj, groupObj):
    """
    Will determine is a user is a member of a group. Returns ``Tru`` or ``False``
    """
    if userObj.groups:
        if groupObj in userObj.groups:
            return True
        else:
            return False
    else:
        return False

def add_to_group(userObj, groupObj):
    """
    Will add a group object to the groups list in the User object. returns a ``Mojo.Auth.models.User`` object.
    """
    if not is_member_of(userObj, groupObj):
        if userObj.groups:
            userObj.groups.append(groupObj)
        else:
            userObj.groups = [groupObj]

        return userObj
    else:
        raise ValueError('This user is already a member of this group')

def remove_from_group(userObj, groupObj):
    """
    Removes a user from the group, returns ``True`` if successful, ``False`` if the user is not a member of the group
    """
    if is_member_of(userObj, groupObj):
        userObj.groups.remove(groupObj)
        return True
    else:
        return False

