from flask import g,request
from flask_httpauth import HTTPTokenAuth
from werkzeug.exceptions import NotFound,Unauthorized

from flask_restplus import Resource
from app.utils import api

from serializers import bucketlist,bucketlist_item
from controller import (create_bucket_list,get_all_bucketlists,
                       get_single_bucketlist,delete_bucket_list,
                       get_single_bucketlist_item,
                       update_bucket_list,create_bucket_list_item,
                       update_bucket_list_item,delete_bucket_list_items)
from app.users.models import User

token_auth = HTTPTokenAuth('Bearer')

namespace = api.namespace('bucketlist',description='BucketList operations')



@token_auth.verify_token
def verify_token(token):
    user = User.verify_auth_token(token)
    if not user or type(user)!= User:
        raise Unauthorized("Not Authorized")
        return False
    g.user = user
    print(g.user)
    return True



@namespace.route('/')
class BucketListResource(Resource):
    @api.marshal_list_with(bucketlist)
    @token_auth.login_required
    def get(self):
        return get_all_bucketlists(g.user.id)

    @api.expect(bucketlist)
    @token_auth.login_required
    def post(self):
        """
        Creates new bucketlist

        """
        data = request.get_json(force = True)
        create_bucket_list(g.user.id,data)
        return  200

@namespace.route('/<int:id>')
@namespace.param('id','BucketList identifier')
class SingleBucketListResource(Resource):
    @token_auth.login_required
    @api.marshal_with(bucketlist)
    def get(self,id):
        if get_single_bucketlist(id,g.user.id) == "Bucketlist doesn't exist":
            raise NotFound("Bucketlist doesn't exist")
        return get_single_bucketlist(id,g.user.id)
    @token_auth.login_required
    def delete(self,id):
        if get_single_bucketlist(id,g.user.id) == "Bucketlist doesn't exist":
            raise NotFound("Bucketlist doesn't exist")
        return delete_bucket_list(id,g.user.id), 200
    @token_auth.login_required
    @api.expect(bucketlist)
    def put(self,id):
        if get_single_bucketlist(id,g.user.id) == "Bucketlist doesn't exist":
            raise NotFound("Bucketlist doesn't exist")
        data = request.get_json(force = True)
        update_bucket_list(id,g.user.id,data)
        return 200

@namespace.route('/<int:id>/items')
@namespace.param('id','BucketList identifier')
class BucketListItemsResource(Resource):
    @token_auth.login_required
    @api.expect(bucketlist_item)
    def post(self,id):
        data = request.get_json(force = True)
        if get_single_bucketlist(id,g.user.id) == "Bucketlist doesn't exist":
            raise NotFound("Bucketlist doesn't exist")
        create_bucket_list_item(data,id,g.user.id)
        return 200


@namespace.route('/<int:id>/items/<int:item_id>')
@namespace.param(('id','BucketList identifier'),('item_id','BucketListItem identifier'))
class BucketListItemsResource(Resource):
    @token_auth.login_required
    @api.expect(bucketlist_item)
    def put(self,id,item_id):
        data = request.get_json(force = True)
        if get_single_bucketlist(id,g.user.id) == "Bucketlist doesn't exist":
            raise NotFound("Bucketlist doesn't exist")
        elif get_single_bucketlist_item(id,item_id) == "Item doesn't exist":
            raise NotFound("Item does not exist")
        update_bucket_list_item(id,item_id,data)
        return 200
    @token_auth.login_required
    def delete(self,id,item_id):
        if get_single_bucketlist(id,g.user.id) == "Bucketlist doesn't exist":
            raise NotFound("Bucketlist doesn't exist")
        elif get_single_bucketlist_item(id,item_id) == "Item doesn't exist":
            raise NotFound("Item does not exist")
        return delete_bucket_list_items(id,item_id),200
