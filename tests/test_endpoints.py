import unittest
from app import create_app,db


class BucketListEndpointTestcase(unittest.TestCase):
    """Tests for  BucketList Endpoints."""
    def setUp(self):
        self.app = create_app('testing')
        self.client = self.app.test_client
        self.bucketlist = '{"title":"Road Trip","description":"Stuff to do on my road trip"}'
        self.app_context = self.app.app_context()
        self.app_context.push()

        db.create_all()

    def test_bucket_list_creation_endpoint(self):
        response = self.client().post('/bucketlist/',data=self.bucketlist,
                                        content_type="application/json")
        self.assertEqual(response.status_code,200)


    def test_all_bucket_lists_end_point(self):
        self.client().post('/bucketlist/',data=self.bucketlist,
                                                content_type="application/json")
        response = self.client().get('/bucketlist/')
        self.assertEqual(response.status_code,200)


    def test_get_single_bucket_list_endpoint(self):
        self.client().post('/bucketlist/',data=self.bucketlist,
                                                content_type="application/json")
        response = self.client().get('/bucketlist/1')
        self.assertEqual(response.status_code,200)

    def test_get_single_bucket_list_with_nonexistent_id(self):
        response = self.client().get('/bucketlist/19')
        self.assertIn('{"message": "Bucketlist doesn\'t exist"}',response.data)

    def test_delete_single_bucket_list_endpoint(self):
        self.client().post('/bucketlist/',data=self.bucketlist,
                                                content_type="application/json")
        response = self.client().delete('/bucketlist/1')

        self.assertEqual(response.status_code,200)
        response = self.client().get('/bucketlist/1')
        self.assertIn('{"message": "Bucketlist doesn\'t exist"}',response.data)

    def test_delete_non_existent_bucket_list_endpoint(self):
        response = self.client().delete('/bucketlist/1')

        self.assertEqual(response.status_code,404)
        self.assertIn('{"message": "Bucketlist doesn\'t exist"}',response.data)
















    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()



if __name__ == '__main__':
    unittest.main()
