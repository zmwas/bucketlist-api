 from flask_restplus import fields

from app.utils import api


bucket = api.model('BucketList', {
    'title':fields.String(required=True,description='Name of the bucketlist'),
    'description':fields.String(required=False,description='A short snippet describing the bucketlist'),
})


bucketlist_item = api.model('BucketListItem',{
    'name': fields.Integer(required=True,description="Name of the bucketlist item")
})

bucketlist = api.model('BucketList', {
    'title':fields.String(required=True,description='Name of the bucketlist'),
    'description':fields.String(required=False,description='A short snippet describing the bucketlist'),
    'items':fields.List(fields.Nested(bucketlist_item))
})
