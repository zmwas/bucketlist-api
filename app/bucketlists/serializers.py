from flask_restplus import fields

from app.utils import api


bucket = api.model('BucketList', {
    'title':fields.String(required=True,description='Name of the bucketlist'),
    'description':fields.String(required=False,description='A short snippet describing the bucketlist'),
})


bucketlistitems = api.model('BucketListItem',{
    'id':fields.Integer(),
    'name': fields.String(required=True,description="Name of the bucketlist item")
})

bucketlist = api.model('Bucket List', {
    'id':fields.Integer(),
    'title':fields.String(required=True,description='Name of the bucketlist'),
    'description':fields.String(required=False,description='A short snippet describing the bucketlist'),
    'bucketlistitems': fields.List(fields.Nested(bucketlistitems)),
})
