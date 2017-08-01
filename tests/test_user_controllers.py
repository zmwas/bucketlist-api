import unittest

from app.users.models import User
from app import create_app,db
from app.users.controller import create_user

class UserTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app("testing")
        print self.app
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.user ={"email":"zac@gmail.com","password":"hunter123"}

        db.create_all()

    def test_user_creation(self):
        users_1 = User.query.all()
        create_user(self.user)
        users_2 = User.query.all()
        self.assertEqual(len(users_1)+1,len(users_2))
        self.assertTrue(len(users_2)>len(users_1))

    def test_user_creation_with_existent_email_returns_error(self):
        create_user(self.user)
        data ={"email":"zac@gmail.com","password":"password123"}

        self.assertEqual(create_user(data),"User with that email exists")
    def test_user_creation_with_no_email_returns_error(self):
        data ={"email":"","password":"password123"}
        self.assertEqual(create_user(data),"Please enter all details")

    def test_user_creation_with_no_password_returns_error(self):
        data ={"email":"zac@gmail.com","password":""}
        self.assertEqual(create_user(data),"Please enter all details")

    def test_user_creation_with_short_password_returns_error(self):
        data ={"email":"zac@gmail.com","password":"pass"}
        self.assertEqual(create_user(data),"Password should be at least 8 characters long")

        


    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
