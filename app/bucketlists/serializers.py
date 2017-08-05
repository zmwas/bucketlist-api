from flask_restplus import fields

from app.utils import api


bucketlist = api.model('BucketList', {
    'id':fields.Integer(read_only=True,description='Unique identifier for the bucketlist'),
    'title':fields.String(required=True,description='Name of the bucketlist'),
    'description':fields.String(required=False,description='A short snippet describing the bucketlist')
})

bucketlist_item = api.model('BucketListItem',{
    'id':fields.Integer(read_only=True,description='Unique identifier for the bucketlist item'),
    'name': fields.Integer(required=True,description="Name of the bucketlist item")
})
