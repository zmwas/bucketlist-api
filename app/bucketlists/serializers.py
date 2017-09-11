from flask_restplus import fields

from app.utils import api

#serializer for bucket model
bucket = api.model('BucketList', {
    'title':fields.String(required=True,description='Name of the bucketlist'),
    'description':fields.String(required=False,description='A short snippet describing the bucketlist'),
})

#serializer for bucketlist item model
bucketlistitems = api.model('BucketListItem',{
    'id':fields.Integer(),
    'name': fields.String(required=True,description="Name of the bucketlist item")
})

#serializer for bucket response
bucketlist = api.model('Bucket List', {
    'id':fields.Integer(),
    'title':fields.String(required=True,description='Name of the bucketlist'),
    'description':fields.String(required=False,description='A short snippet describing the bucketlist'),
    'bucketlistitems': fields.List(fields.Nested(bucketlistitems)),
})

response = api.model('Response',{
    'status':fields.String(),
    'pages':fields.Integer(),
    'data': fields.List(fields.Nested(bucketlist))
})
