import unittest
from sqlalchemy.exc import IntegrityError
from app import create_app,db
from app.bucketlists.models import BucketList
from app.bucketlists.controller import create_bucket_list

class BucketListTestCase(unittest.TestCase):

    def setUp(self):
        self.app =  create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()




    def test_bucket_list_creation(self):
        bucketlist = BucketList()
        bucketlist.title = "2017"
        bucketlist.description = "Stuff I want to do in 2017"
        db.session.add(bucketlist)
        db.session.commit()

        queried_bucketlist = BucketList.query.first()
        self.assertIsNotNone(queried_bucketlist)








    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()










if __name__ == '__main__':
    unittest.main()
