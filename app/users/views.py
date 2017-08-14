from flask import g,jsonify,request
from werkzeug.exceptions import BadRequest,Unauthorized

from flask_restplus import Resource
from flask_httpauth import HTTPBasicAuth
from app.utils import api
from serializers import user
from controller import create_user
from models import User


aut = HTTPBasicAuth()




namespace = api.namespace('auth',description='Creation and authentication of users')



@aut.verify_password
def verify_password(email, password):
    user = User.query.filter_by(email=email).first()
    if not user or not user.verify_password_hash(password):
        raise Unauthorized("Not Authorized")
        return False

    g.user = user
    return True



@namespace.route('/register')
class RegisterUserResource(Resource):

    @api.expect(user)
    def post(self):
        """
        Register a user

        """
        data = request.get_json(force = True)
        if create_user(data) == "Please enter all details":
            raise BadRequest("Please enter all details")
        elif create_user(data) == "Password should be at least 8 characters long":
            raise BadRequest("Password should be at least 8 characters long")
        elif create_user(data)=="Please provide a valid email":
             raise BadRequest("Please provide a valid email")
        if User.query.filter_by(email=data.get('email')).first() is not None :
            raise BadRequest("User with that email exists")
        create_user(data)
        return 201

@namespace.route('/login')
class LoginUserResource(Resource):
    @aut.login_required
    def post(self):
        """
        Log in a user

        """
        token = g.user.generate_auth_token()
        return jsonify({'Authorization': token.decode('ascii')})
