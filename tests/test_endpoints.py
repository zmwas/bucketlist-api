import unittest
from app import create_app,db
from config import app_config


class BucketListEndpointTestcase(unittest.TestCase):
    """Tests for  BucketList Endpoints."""
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()
        self.bucketlist = '{"title":"2018","description":"Stuff to do in 2018"}'
        self.bucket_list_item = '{"name":"Finish watching One Pice","bucketlist_id":1}'
        db.create_all()

    def test_bucket_list_creation_endpoint(self):
        response = self.client.post('/bucketlist/',data=self.bucketlist,
                                        content_type="application/json")
        self.assertEqual(response.status_code, 200)


    def test_all_bucket_lists_end_point(self):
        self.client.post('/bucketlist/',data=self.bucketlist,
                                                content_type="application/json")
        response = self.client.get('/bucketlist/')
        self.assertEqual(response.status_code,200)


    def test_get_single_bucket_list_endpoint(self):
        self.client.post('/bucketlist/',data=self.bucketlist,
                                                content_type="application/json")
        response = self.client.get('/bucketlist/1')
        self.assertEqual(response.status_code,200)

    def test_get_single_bucket_list_with_nonexistent_id(self):
        response = self.client.get('/bucketlist/19')
        self.assertIn('{"message": "Bucketlist doesn\'t exist"}\n',response.data)

    def test_delete_single_bucket_list_endpoint(self):
        self.client.post('/bucketlist/',data=self.bucketlist,
                                                content_type="application/json")
        response = self.client.delete('/bucketlist/1')

        self.assertEqual(response.status_code,200)
        response = self.client.get('/bucketlist/1')
        self.assertIn('{"message": "Bucketlist doesn\'t exist"}\n',response.data)

    def test_delete_non_existent_bucket_list_endpoint(self):
        response = self.client.delete('/bucketlist/1')

        self.assertEqual(response.status_code,404)
        self.assertIn('{"message": "Bucketlist doesn\'t exist"}\n',response.data)

    def test_update_single_bucket_list_endpoint(self):
        self.client.post('/bucketlist/',data=self.bucketlist,
                                                content_type="application/json")
        data='{"title":"2017","description":"Stuff to do in 2017"}'
        response = self.client.put('/bucketlist/1',data=data,
                                                content_type="application/json")
        self.assertEqual(response.status_code,200)

    def test_update_non_existent_bucket_list_endpoint(self):
        data='{"title":"2017","description":"Stuff to do in 2017"}'
        response = self.client.put('/bucketlist/1',data=data,
                                                content_type="application/json")
        self.assertEqual(response.status_code,404)

    def test_bucket_list_item_creation_endpoint(self):
        self.client.post('/bucketlist/',data=self.bucketlist,
                                            content_type="application/json")
        response = self.client.post('/bucketlist/1/items',
                                    data=self.bucket_list_item,
                                    content_type="application/json")
        self.assertEqual(response.status_code,200)

    def test_item_creation_with_non_existent_bucketlist_id_returns_404(self):
        response = self.client.post('/bucketlist/1/items',
                                    data=self.bucket_list_item,
                                    content_type="application/json")
        self.assertEqual(response.status_code,404)


    def test_update_single_bucketlist_item_endpoint(self):
        self.client.post('/bucketlist/',data=self.bucketlist,
                                                content_type="application/json")
        self.client.post('/bucketlist/1/items',data=self.bucket_list_item,
                                    content_type="application/json")
        data = '{"name":"Finish watching Fairy Tail"}'
        response=self.client.put('/bucketlist/1/items/1',data=data,
                                    content_type="application/json")
        self.assertEqual(response.status_code,200)
    def test_update_item_with_non_existent_bucketlist_item_id_returns_404(self):
        data = '{"name":"Finish watching Fairy Tail"}'
        response=self.client.put('/bucketlist/1/items/76',data=data,
                                    content_type="application/json")
        self.assertEqual(response.status_code,404)
    def test_update_item_with_non_existent_bucketlist_id_returns_404(self):
        data = '{"name":"Finish watching Fairy Tail"}'
        response=self.client.put('/bucketlist/1/items/76',data=data,
                                    content_type="application/json")
        self.assertEqual(response.status_code,404)


    def test_delete_single_bucket_list_item_endpoint(self):
        self.client.post('/bucketlist/',data=self.bucketlist,
                                                content_type="application/json")
        self.client.post('/bucketlist/1/items',data=self.bucket_list_item,
                                    content_type="application/json")
        response = self.client.delete('/bucketlist/1/items/1')
        self.assertEqual(response.status_code,200)

    def test_delete_item_with_non_existent_bucketlist_item_id_returns_404(self):
        response = self.client.delete('/bucketlist/1/items/1')
        self.assertEqual(response.status_code,404)

    def test_delete_item_with_non_existent_bucketlist_id_returns_404(self):
        response = self.client.delete('/bucketlist/1/items/1')
        self.assertEqual(response.status_code,404)











    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()


if __name__ == '__main__':
    unittest.main()
