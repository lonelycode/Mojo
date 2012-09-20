import unittest
import datetime

from Mojo.Auth.models import User, Group
from Mojo.Auth.AuthManager import *

testGroup = Group({
    'group_name' : u'testGroup'
})

new_group = Group({
    'group_name':u'second_group'
})

testUser = User({
    'username':u'testuser',
    'password': u'$2a$12$mwFMSikk.7YgXbzCFYIjNeTthsmDMBunwdkYQiIkk38c2gji/c7N.',
    'email':u'test@test.com',
    'groups':[testGroup],
    'active':True,
    'profile':None,
    'is_superuser':False,
    'last_login':datetime.datetime.now(),
    'date_joined':datetime.datetime.now(),
    })

testSuperUser = User({
    'username':u'testuser',
    'password': u'$2a$12$mwFMSikk.7YgXbzCFYIjNeTthsmDMBunwdkYQiIkk38c2gji/c7N.',
    'email':u'test@test.com',
    'groups':None,
    'active':True,
    'profile':None,
    'is_superuser':True,
    'last_login':datetime.datetime.now(),
    'date_joined':datetime.datetime.now(),
    })

class AuthManagerTest(unittest.TestCase):

    def test_authenticate_positive(self):
        self.assertEqual(authenticate(testUser, u'realpasswd'), True)

    def test_authenticate_negative(self):
        self.assertEqual(authenticate(testUser, u'fakepasswd'), False)

    def test_set_password(self):
        real_password = u'realpasswd_changed'
        temp_UserObj = set_password(testUser, real_password)
        self.assertEqual(authenticate(temp_UserObj, u'realpasswd_changed'), True)

    def test_make_random_password(self):
        pw = make_random_password()
        pwlen = len(pw)
        self.assertEqual(pwlen, 8)

    def test_login(self):
        tempUserObj = login(testUser)
        now = datetime.datetime.now()
        ten_seconds_in_past = now - datetime.timedelta(seconds =10)

        isInRange = False
        if tempUserObj.last_login < now:
            if tempUserObj.last_login > ten_seconds_in_past:
                isInRange = True

        self.assertEqual(isInRange, True)


    def test_is_member_of(self):

        checkMember = is_member_of(testUser,testGroup)

        self.assertEqual(checkMember, True)

    def test_add_to_group(self):
        thisUser = add_to_group(testUser, new_group)

        inGroup = False
        if is_member_of(thisUser, new_group):
            inGroup = True

        self.assertEqual(inGroup, True)

    def test_remove_from_group(self):
        returnedUser = remove_from_group(testUser, new_group)

        inGroup = True
        if not is_member_of(returnedUser, new_group):
            inGroup = False

        self.assertEqual(inGroup, False)

if __name__ == '__main__':
    unittest.main()