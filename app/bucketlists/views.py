from flask import request
from werkzeug.exceptions import NotFound

from flask_restplus import Resource
from app.utils import api

from serializers import bucketlist,bucketlist_item
from controller import (create_bucket_list,get_all_bucketlists,
                       get_single_bucketlist,delete_bucket_list,
                       get_single_bucketlist_item,
                       update_bucket_list,create_bucket_list_item,
                       update_bucket_list_item,delete_bucket_list_items)

namespace = api.namespace('bucketlist',description='BucketList operations')


@namespace.route('/')
class BucketListResource(Resource):
    @api.marshal_list_with(bucketlist)
    def get(self):
        return get_all_bucketlists()



    @api.expect(bucketlist)
    def post(self):
        """
        Creates new bucketlist

        """
        data = request.get_json(force = True)
        create_bucket_list(data)
        return  200

@namespace.route('/<int:id>')
@namespace.param('id','BucketList identifier')
class SingleBucketListResource(Resource):
    @api.marshal_with(bucketlist)
    def get(self,id):
        if get_single_bucketlist(id) == "Bucketlist doesn't exist":
            raise NotFound("Bucketlist doesn't exist")

        return get_single_bucketlist(id)

    def delete(self,id):
        if get_single_bucketlist(id) == "Bucketlist doesn't exist":
            raise NotFound("Bucketlist doesn't exist")

        return delete_bucket_list(id), 200

    @api.expect(bucketlist)
    def put(self,id):
        if get_single_bucketlist(id) == "Bucketlist doesn't exist":
            raise NotFound("Bucketlist doesn't exist")
        update_bucket_list
        return 200

@namespace.route('/<int:id>/items')
@namespace.param('id','BucketList identifier')
class BucketListItemsResource(Resource):
    @api.expect(bucketlist_item)
    def post(self,id):
        data = request.get_json(force = True)
        if get_single_bucketlist(id) == "Bucketlist doesn't exist":
            raise NotFound("Bucketlist doesn't exist")
        create_bucket_list_item(data)
        return 200


@namespace.route('/<int:id>/items/<int:item_id>')
@namespace.param(('id','BucketList identifier'),('item_id','BucketListItem identifier'))
class BucketListItemsResource(Resource):
    @api.expect(bucketlist_item)
    def put(self,id,item_id):
        data = request.get_json(force = True)
        if get_single_bucketlist_item(id,item_id) == "Item doesn't exist":
            raise NotFound("Item does not exist")
        update_bucket_list_item(id,item_id,data)
        return 200

    def delete(self,id,item_id):
        if get_single_bucketlist_item(id,item_id) == "Item doesn't exist":
            raise NotFound("Item does not exist")
        return delete_bucket_list_items(id,item_id),200
