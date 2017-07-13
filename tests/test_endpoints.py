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
        response = self.client().post('/bucketlist/',data=self.bucketlist,content_type="application/json")
        self.assertEqual(response.status_code,201)






    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()



if __name__ == '__main__':
    unittest.main()
