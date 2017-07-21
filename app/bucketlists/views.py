from flask import request
from werkzeug.exceptions import NotFound

from flask_restplus import Resource
from app.utils import api

from serializers import bucketlist
from controller import (create_bucket_list,get_all_bucketlists,
                       get_single_bucketlist,delete_bucket_list)

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
