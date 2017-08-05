from flask_restplus import fields
from app.utils import api


user = api.model('User',{
    'id':fields.Integer(read_only=True,description='Unique identifier for a user'),
    'email':fields.String(required=True,description='Email of the user'),
    'password_hash':fields.String(read_only=True)
})
