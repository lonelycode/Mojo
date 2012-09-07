import bcrypt, string, random, datetime

def authenticate(userObj, password):
    """
    Will check if a user password matches the input to authenticate the user,
    this will NOT log them in
    """
    if bcrypt.hashpw(password, userObj.password) == userObj.password:
        return True
    else:
        return False

def set_password(userObj, new_password):
    """
    Sets the user password - requires bcrypt
    """
    new_pw = bcrypt.hashpw(new_password, bcrypt.gensalt())
    userObj.password = new_pw

    return UserObj

def make_random_password():
    """
    Returns a simple random password as string
    """
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(8))

def login(userObj):
    """
    Set the appropriate state of the user object
    """
    userObj.last_login = datetime.datetime.now()

    return userObj