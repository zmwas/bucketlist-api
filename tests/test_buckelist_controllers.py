import unittest
from app import create_app, db
from app.bucketlists.models import BucketList
from app.bucketlists.controller import (create_bucket_list, get_all_bucketlists,
                                        get_single_bucketlist,
                                        delete_bucket_list,update_bucket_list
                                        )
from config import app_config

class BucketListTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app("testing")
        self.app.config.from_object(app_config["testing"])
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.bucket_list = {"title":"Road Trip", "description":"Stuff to do on my road trip"}

        db.create_all()

    def test_bucket_list_creation(self):
        create_bucket_list(self.bucket_list)
        queried_bucketlist = BucketList.query.first()
        self.assertIsNotNone(queried_bucketlist)
        self.assertTrue(queried_bucketlist)

    def test_get_all_bucket_lists(self):
        all_bucket_lists = BucketList.query.all()
        self.assertEqual(get_all_bucketlists(),all_bucket_lists)


    def test_get_single_bucket_list(self):
        create_bucket_list(self.bucket_list)
        single_bucket_list = BucketList.query.get(1)

        self.assertEqual(get_single_bucketlist(1),single_bucket_list)

    def test_get_single_bucket_list_with_nonexistent_id(self):
        create_bucket_list(self.bucket_list)
        single_bucket_list = BucketList.query.get(2)

        self.assertEqual(get_single_bucketlist(2),"Bucketlist doesn't exist")

    def test_delete_single_bucket_list(self):
        create_bucket_list(self.bucket_list)
        delete_bucket_list(1)
        all_bucket_lists = BucketList.query.all()

        self.assertEqual(len(all_bucket_lists),0)

    def test_delete_non_existent_bucket_list(self):
        create_bucket_list(self.bucket_list)

        self.assertEqual(delete_bucket_list(2),"Bucketlist doesn't exist")

    def test_update_bucketlist(self):
        create_bucket_list(self.bucket_list)
        data =
        update_bucket_list(1,)
        self.assertEqual()



    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()


if __name__ == '__main__':
    unittest.main()
