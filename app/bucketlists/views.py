from flask import request
from flask_restplus import Resource
from app.utils import api

from serializers import bucketlist
from controller import create_bucket_list,get_all_bucketlists

namespace = api.namespace('bucketlist',description='Operations related to bucketlists')


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
        return None, 201
