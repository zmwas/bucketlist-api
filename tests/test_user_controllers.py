import unittest

from app.users.models import User
from app import create_app,db
from app.users.controller import create_user

class UserTestCase(unittest.TestCase):
    """Tests for  user controllers"""

    def setUp(self):
        """Set up user variable for tests"""
        self.app = create_app("testing")
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.user ={"email":"zac@gmail.com","password":"hunter123"}

        db.create_all()

    def test_user_creation(self):
        """Test user creation"""
        users_1 = User.query.all()
        create_user(self.user)
        users_2 = User.query.all()
        self.assertEqual(len(users_1)+1,len(users_2))
        self.assertTrue(len(users_2)>len(users_1))

    def test_user_creation_with_existent_email_returns_error(self):
        """Test user is not created if email is similar"""
        create_user(self.user)
        data ={"email":"zac@gmail.com","password":"password123"}

        self.assertEqual(create_user(data),"User with that email exists")
    def test_user_creation_with_no_email_returns_error(self):
        """Test user is not created if email is not sent"""
        data ={"email":"","password":"password123"}
        self.assertEqual(create_user(data),"Please enter all details")

    def test_user_creation_with_no_password_returns_error(self):
        """Test user is not created if password is not sent"""
        data ={"email":"zac@gmail.com","password":""}
        self.assertEqual(create_user(data),"Please enter all details")

    def test_user_creation_with_short_password_returns_error(self):
        """Test user is not created if password is too short"""
        data ={"email":"zac@gmail.com","password":"pass"}
        self.assertEqual(create_user(data),"Password should be at least 8 characters long")
    def test_user_creation_with_no_email_returns_error(self):
        """Test user is not created if wrong email format is used"""
        data ={"email":"wetydyvtde","password":"password123"}
        self.assertEqual(create_user(data),"Please provide a valid email")




    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
