from flask_restplus import fields
from app.utils import api


user = api.model('User',{
    'email':fields.String(required=True,description='Email of the user'),
    'password':fields.String(write_only=True)
})
