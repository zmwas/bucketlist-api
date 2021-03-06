import unittest
from app import create_app, db
from app.bucketlists.models import BucketList,BucketListItem
from app.bucketlists.controller import (create_bucket_list, get_all_bucketlists,
                                        get_single_bucketlist,
                                        delete_bucket_list,update_bucket_list,
                                        create_bucket_list_item,
                                        update_bucket_list_item,
                                        delete_bucket_list_items

                                        )
from config import app_config
from app.users.models import User
from app.users.controller import create_user


class BucketListTestCase(unittest.TestCase):
    """ Tests for bucket list controller methods """
    def setUp(self):
        """Set up variables for tests"""
        self.app = create_app("testing")
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.bucket_list = {"title":"Road Trip", "description":"Stuff to do on my road trip"}
        self.bucket_list_item = {"name":"Go to Mombasa","bucketlist_id":1}
        self.user ={"email":"zac@gmail.com","password":"hunter123"}
        self.user_2 ={"email":"zack@gmail.com","password":"hunter123"}



        db.create_all()

    def test_bucket_list_creation(self):
        """Tests that bucket list is created """
        create_user(self.user)
        user=User.query.first()
        create_bucket_list(1,self.bucket_list)
        queried_bucketlist = BucketList.query.first()
        self.assertIsNotNone(queried_bucketlist)
        self.assertTrue(queried_bucketlist)

    def test_bucket_list_creation_with_similar_title(self):
        """ Tests that bucket list with same title is not created"""
        create_user(self.user)
        create_bucket_list(1,self.bucket_list)
        duplicate = {"title":"Road Trip"}
        self.assertEqual(create_bucket_list(1,duplicate),"Similar bucketlist title")



    def test_get_single_bucket_list(self):
        """ Tests that bucket list is fetched"""

        create_user(self.user)
        create_bucket_list(1,self.bucket_list)
        single_bucket_list = BucketList.query.get(1)

        self.assertEqual(get_single_bucketlist(1,1),single_bucket_list)

    def test_get_single_bucket_list_with_nonexistent_id(self):
        """ Tests that bucket list with non existent id is not fetched"""

        create_user(self.user)
        create_bucket_list(1,self.bucket_list)

        self.assertEqual(get_single_bucketlist(2,1),"Bucketlist doesn't exist")

    def test_delete_single_bucket_list(self):
        """ Tests that bucket list is deleted"""
        create_user(self.user)
        create_bucket_list(1,self.bucket_list)
        delete_bucket_list(1,1)
        all_bucket_lists = BucketList.query.all()

        self.assertEqual(len(all_bucket_lists),0)

    def test_delete_non_existent_bucket_list(self):
        """ Tests that bucket list is not deleted"""
        create_user(self.user)
        create_bucket_list(1,self.bucket_list)

        self.assertEqual(delete_bucket_list(2,1),"Bucketlist doesn't exist")

    def test_update_bucketlist(self):
        """ Tests that bucket list is updated"""
        create_user(self.user)
        create_bucket_list(1,self.bucket_list)
        data = {"title":"2017", "description":"Stuff to do in 2017"}

        update_bucket_list(1,1,data)
        new_bucket_list_title =BucketList.query.get(1).title

        self.assertEqual(new_bucket_list_title,"2017")

    def test_create_bucket_list_item(self):
        """ Tests that bucket list item is created"""
        create_user(self.user)
        create_bucket_list(1,self.bucket_list)

        create_bucket_list_item(self.bucket_list_item,1,1)
        queried_item = BucketListItem.query.first()
        self.assertIsNotNone(queried_item)
        self.assertTrue(queried_item)

    def test_update_bucketlist_item(self):
        """ Tests that bucket list item is updated"""
        create_user(self.user)
        create_bucket_list(1,self.bucket_list)
        create_bucket_list_item(self.bucket_list_item,1,1)
        data = {"name":"Go to Mara"}
        update_bucket_list_item(1,1,data)
        new_bucket_list_item_name = BucketListItem.query.get(1).name

        self.assertEqual(new_bucket_list_item_name,"Go to Mara")

    def test_delete_single_bucket_list_item(self):
        """ Tests that bucket list item is deleted"""
        create_user(self.user)
        create_bucket_list(1,self.bucket_list)
        create_bucket_list_item(self.bucket_list_item,1,1)
        delete_bucket_list_items(1,1)
        all_bucket_list_item = BucketListItem.query.all()
        self.assertEqual(len(all_bucket_list_item),0)


    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
