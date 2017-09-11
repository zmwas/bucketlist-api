import unittest
import json
from base64 import b64encode
from app import create_app,db
from config import app_config


class BucketListEndpointTestcase(unittest.TestCase):
    """Tests for  BucketList Endpoints."""
    def setUp(self):
        """ Set up variables for tests """
        self.app = create_app("testing")
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()
        db.create_all()

        self.bucketlist = '{"title":"2018","description":"Stuff to do in 2018"}'
        self.bucket_list_item = '{"name":"Finish watching One Piece"}'
        self.user = '{"email":"zac@gmail.com","password":"hunter123"}'
        self.headers_basic = {
           'Authorization': 'Basic ' + b64encode("{0}:{1}".format("zac@gmail.com", "hunter123"))
           }
        self.registered_user = self.client.post('/auth/register',data=self.user,
                                   content_type="application/json")
        self.login_response = self.client.post('auth/login',
                                               content_type="application/json",
                                               headers=self.headers_basic)

        self.login_response_json = json.loads(self.login_response.data
                                              .decode('utf-8'))
        self.token = self.login_response_json["Authorization"]
        self.headers_auth = {'Authorization': 'Bearer ' + self.token}


    def test_bucket_list_creation_endpoint(self):
        """Test that a bucketList successfully created and message is returned"""
        response = self.client.post('/bucketlist/',data=self.bucketlist,
                                        content_type="application/json",
                                        headers=self.headers_auth
                                        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(json.loads(response.data)["status"],
                         "BucketList successfully created")


    def test_bucket_list_creation_with_empty_string_endpoint_returns_400(self):
        """Test that a bucketList with no title is not created and message is returned """
        bucketlist = '{"title":"        ","description":"Stuff to do in 2018"}'
        response = self.client.post('/bucketlist/',data=bucketlist,
                                        content_type="application/json",
                                        headers=self.headers_auth
                                        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json.loads(response.data)["message"],
                         "Please provide a title for your bucketlist")

    def test_bucket_list_creation_endpoint_with_similar_title_returns_400(self):
        """Test that a bucketList with a similar title is not created and message is returned """
        self.client.post('/bucketlist/',data=self.bucketlist,
                                        content_type="application/json",
                                        headers=self.headers_auth
                                        )
        response=self.client.post('/bucketlist/',data=self.bucketlist,
                                        content_type="application/json",
                                        headers=self.headers_auth
                                        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json.loads(response.data)["message"],
                         "A bucketlist with that name exists")

    def test_bucketlist_pagination(self):
        """Test that fetched bucketLists are paginated when returned"""
        self.client.post('/bucketlist/',data=self.bucketlist,
                                                content_type="application/json",
                                                headers=self.headers_auth)
        response = self.client.get('/bucketlist/?page=1&per_page=10',
                                   headers=self.headers_auth)
        self.assertEqual(response.status_code,200)
        self.assertEqual(len(json.loads(response.data)["data"]),1)


    def test_bucketlist_search_with_right_term_returns_200(self):
        """Test that a searched bucketList that exists is returned """
        self.client.post('/bucketlist/',data=self.bucketlist,
                                                content_type="application/json",
                                                headers=self.headers_auth)
        response = self.client.get('/bucketlist/?q=201&page=1&per_page=10',
                                   headers=self.headers_auth)
        self.assertEqual(response.status_code,200)
        self.assertEqual(len(json.loads(response.data)["data"]),1)

    def test_bucketlist_search_with_wrong_term_returns_404(self):
        """
            Test that a searched bucketList that  does not exist returns 404
            and a message is returned
         """
        self.client.post('/bucketlist/',data=self.bucketlist,
                                                content_type="application/json",
                                                headers=self.headers_auth)
        response = self.client.get('/bucketlist/?q=hgqpage=1&per_page=10',
                                   headers=self.headers_auth)
        self.assertEqual(response.status_code,404)
        self.assertEqual(json.loads(response.data)["message"],
                         "Bucketlist doesn't exist")

    def test_all_bucket_lists_end_point(self):
        """Test that fetching all bucketLists """

        self.client.post('/bucketlist/',data=self.bucketlist,
                                                content_type="application/json",
                                                headers=self.headers_auth)
        response = self.client.get('/bucketlist/',headers=self.headers_auth)
        self.assertEqual(response.status_code,200)
        self.assertEqual(len(json.loads(response.data)["data"]),1)



    def test_get_single_bucket_list_endpoint(self):
        """Test that fetching a single bucketLists returns the bucketlist"""
        self.client.post('/bucketlist/',data=self.bucketlist,
                                                content_type="application/json",
                                                headers=self.headers_auth)
        response = self.client.get('/bucketlist/1',headers=self.headers_auth)
        self.assertEqual(response.status_code,200)
        self.assertEqual(json.loads(response.data)["id"],1)

    def test_get_single_bucket_list_with_nonexistent_id(self):
        """
        Test that fetching a single bucketLists with a wrong id returns error

        """
        response = self.client.get('/bucketlist/19',headers=self.headers_auth)
        self.assertIn('{"message": "Bucketlist doesn\'t exist"}\n',response.data)

    def test_delete_single_bucket_list_endpoint(self):
        """
        Test that deleting a single bucketLists

        """
        self.client.post('/bucketlist/',data=self.bucketlist,
                                                content_type="application/json",
                                                headers=self.headers_auth)
        response = self.client.delete('/bucketlist/1',headers=self.headers_auth)

        self.assertEqual(response.status_code,200)
        self.assertEqual(json.loads(response.data)["message"],
                         "BucketList successfully deleted")
        response = self.client.get('/bucketlist/1',headers=self.headers_auth)
        self.assertIn('{"message": "Bucketlist doesn\'t exist"}\n',response.data)

    def test_delete_non_existent_bucket_list_endpoint(self):
        """
        Test that deleting a single bucketLists with a wrong id returns error

        """
        response = self.client.delete('/bucketlist/1',headers=self.headers_auth)

        self.assertEqual(response.status_code,404)
        self.assertIn('{"message": "Bucketlist doesn\'t exist"}\n',response.data)

    def test_update_single_bucket_list_endpoint(self):
        """
        Test that updating a single bucketLists

        """
        self.client.post('/bucketlist/',data=self.bucketlist,
                                        content_type="application/json",
                                        headers=self.headers_auth)
        data='{"title":"2017","description":"Stuff to do in 2017"}'
        response = self.client.put('/bucketlist/1',data=data,
                                                content_type="application/json",
                                                headers=self.headers_auth)
        self.assertEqual(response.status_code,200)
        self.assertEqual(json.loads(response.data)["status"],
                         "BucketList successfully updated")

    def test_update_non_existent_bucket_list_endpoint(self):
        """
        Test that updating a single bucketLists with a wrong id returns error

        """
        data='{"title":"2017","description":"Stuff to do in 2017"}'
        response = self.client.put('/bucketlist/1',data=data,
                                                content_type="application/json",
                                                headers=self.headers_auth)
        self.assertEqual(response.status_code,404)
        self.assertEqual(json.loads(response.data)["message"],
                         "Bucketlist doesn't exist")

    def test_bucket_list_item_creation_endpoint(self):
        """
        Test bucket list item creation
        """
        self.client.post('/bucketlist/',data=self.bucketlist,
                                            content_type="application/json",
                                            headers=self.headers_auth)
        response = self.client.post('/bucketlist/1/items',
                                    data=self.bucket_list_item,
                                    content_type="application/json",
                                    headers=self.headers_auth)
        self.assertEqual(response.status_code,201)
        self.assertEqual(json.loads(response.data)["status"],
                         "BucketList item successfully created")
    def test_bucket_list_item_creation_endpoint_with_similar_name_returns_400(self):
        """
        Test that creating a  bucketLists item with a similar name returns error

        """
        self.client.post('/bucketlist/',data=self.bucketlist,
                                            content_type="application/json",
                                            headers=self.headers_auth)
        self.client.post('/bucketlist/1/items',
                                    data=self.bucket_list_item,
                                    content_type="application/json",
                                    headers=self.headers_auth)
        response = self.client.post('/bucketlist/1/items',
                                    data=self.bucket_list_item,
                                    content_type="application/json",
                                    headers=self.headers_auth)

        self.assertEqual(response.status_code,400)
        self.assertEqual(json.loads(response.data)["message"],
                         "Item with that name exists")
    def test_bucket_list_item_creation_endpoint_with_empty_name_returns_400(self):
        """
        Test that creating a  bucketLists item with a no name returns error

        """
        self.client.post('/bucketlist/',data=self.bucketlist,
                                            content_type="application/json",
                                            headers=self.headers_auth)
        bucket_list_item = '{"name":"     "}'
        response = self.client.post('/bucketlist/1/items',
                                    data=bucket_list_item,
                                    content_type="application/json",
                                    headers=self.headers_auth)
        self.assertEqual(response.status_code,400)
        self.assertEqual(json.loads(response.data)["message"],
                         "Please provide a name for the item")

    def test_item_creation_with_non_existent_bucketlist_id_returns_404(self):
        """
        Test that creating a  bucketLists item with a non existent bucketList returns error

        """
        response = self.client.post('/bucketlist/1/items',
                                    data=self.bucket_list_item,
                                    content_type="application/json",
                                    headers=self.headers_auth)
        self.assertEqual(response.status_code,404)
        self.assertEqual(json.loads(response.data)["message"],
                         "Bucketlist doesn't exist")


    def test_update_single_bucketlist_item_endpoint(self):
        """
        Test that updating a  bucketLists item

        """
        self.client.post('/bucketlist/',data=self.bucketlist,
                                                content_type="application/json",
                                                headers=self.headers_auth)
        self.client.post('/bucketlist/1/items',data=self.bucket_list_item,
                                    content_type="application/json",
                                    headers=self.headers_auth)
        data = '{"name":"Finish watching Fairy Tail"}'
        response=self.client.put('/bucketlist/1/items/1',data=data,
                                    content_type="application/json",
                                    headers=self.headers_auth)
        self.assertEqual(response.status_code,200)
        self.assertEqual(json.loads(response.data)["status"],
                         "BucketList item successfully updated")

    def test_update_item_with_non_existent_bucketlist_item_id_returns_404(self):
        """
        Test that updating a  bucketLists item with a non existent id returns error

        """
        data = '{"name":"Finish watching Fairy Tail"}'
        response=self.client.put('/bucketlist/1/items/76',data=data,
                                    content_type="application/json",
                                    headers=self.headers_auth)
        self.assertEqual(response.status_code,404)
        self.assertEqual(json.loads(response.data)["message"],
                         "Bucketlist doesn't exist")

    def test_update_item_with_non_existent_bucketlist_id_returns_404(self):
        """
        Test that updating a  bucketLists item with a non existent id returns error

        """
        data = '{"name":"Finish watching Fairy Tail"}'
        response=self.client.put('/bucketlist/1/items/76',data=data,
                                    content_type="application/json",
                                    headers=self.headers_auth)
        self.assertEqual(response.status_code,404)
        self.assertEqual(json.loads(response.data)["message"],
                         "Bucketlist doesn't exist")


    def test_delete_single_bucket_list_item_endpoint(self):
        """
        Test that deleting a  bucketLists item

        """
        self.client.post('/bucketlist/',data=self.bucketlist,
                                                content_type="application/json",
                                                headers=self.headers_auth)
        self.client.post('/bucketlist/1/items',data=self.bucket_list_item,
                                    content_type="application/json",
                                    headers=self.headers_auth)
        response = self.client.delete('/bucketlist/1/items/1',
                                      headers=self.headers_auth)
        self.assertEqual(response.status_code,200)
        self.assertEqual(json.loads(response.data)["message"],
                         "BucketList item successfully deleted")

    def test_delete_item_with_non_existent_bucketlist_item_id_returns_404(self):
        """
        Test that deleting a  bucketLists item with a non existent id returns error

        """
        response = self.client.delete('/bucketlist/1/items/1',
                                      headers=self.headers_auth)
        self.assertEqual(response.status_code,404)
        self.assertEqual(json.loads(response.data)["message"],
                         "Bucketlist doesn't exist")

    def test_delete_item_with_non_existent_bucketlist_id_returns_404(self):
        """
        Test that deleting a  bucketLists item with a non existent id returns error

        """
        response = self.client.delete('/bucketlist/1/items/1',
                                      headers=self.headers_auth)
        self.assertEqual(response.status_code,404)
        self.assertEqual(json.loads(response.data)["message"],
                         "Bucketlist doesn't exist")

    def test_register_user_endpoint_returns_200(self):
        """
        Test that user is created when data is sent to register

        """
        data = '{"email":"zack@gmail.com","password":"hunter123"}'
        response = self.client.post('/auth/register',data=data,
                                   content_type="application/json")
        self.assertEqual(response.status_code,200)

    def test_register_user_endpoint_with_no_email_returns_400(self):
        """
        Test that user is not created if no email is sent
        """
        data = '{"email":"","password":"hunter123"}'
        response = self.client.post('/auth/register',data=data,
                                        content_type="application/json",
                                        )
        self.assertEqual(response.status_code,400)
        self.assertEqual(json.loads(response.data)["message"],
                         "Please enter all details")

    def test_register_user_endpoint_with_no_password_returns_400(self):
        """
        Test that user is not created if no password is sent
        """
        data = '{"email":"zac@gmail.com","password":""}'
        response = self.client.post('/auth/register',data=data,
                                        content_type="application/json",
                                        )
        self.assertEqual(response.status_code,400)
        self.assertEqual(json.loads(response.data)["message"],
                         "Please enter all details")

    def test_register_user_endpoint_with_short_password_returns_400(self):
        """
        Test that user is not created if short password is sent
        """
        data = '{"email":"zach@gmail.com","password":"zac"}'
        response = self.client.post('/auth/register',data=data,
                                   content_type="application/json")
        self.assertEqual(response.status_code,400)
        self.assertEqual(json.loads(response.data)["message"],
                         "Password should be at least 8 characters long")

    def test_login_user_endpoint_returns_200(self):
        """
        Test that user can login and get a token
        """
        response = self.client.post('/auth/login',
                                     content_type="application/json",
                                     headers=self.headers_basic)
        self.assertEqual(200, response.status_code)
        self.assertTrue(len(json.loads(response.data)["Authorization"])>0)


    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
