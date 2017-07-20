import unittest
from app import create_app,db
from app.bucketlists.models import BucketList
from app.bucketlists.controller import create_bucket_list,get_all_bucketlists

class BucketListTestCase(unittest.TestCase):

    def setUp(self):
        self.app =  create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.bucket_list = {"title":"Road Trip","description":"Stuff to do on my road trip"}

        db.create_all()




    def test_bucket_list_creation(self):
        create_bucket_list(self.bucket_list)
        queried_bucketlist = BucketList.query.first()
        self.assertIsNotNone(queried_bucketlist)
        self.assertTrue(queried_bucketlist)

    def test_get_all_bucket_lists(self):
        all_bucket_lists = BucketList.query.all()
        self.assertEqual(get_all_bucketlists(),all_bucket_lists)







    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()










if __name__ == '__main__':
    unittest.main()
