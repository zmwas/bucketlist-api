import re
from flask import g,jsonify,request
from werkzeug.exceptions import BadRequest,Unauthorized

from flask_restplus import Resource
from flask_httpauth import HTTPBasicAuth
from app.utils import api
from serializers import user
from controller import create_user
from models import User


aut = HTTPBasicAuth()

namespace = api.namespace('auth', description='Creation and authentication of users')

@aut.verify_password
def verify_password(email, password):
    user = User.query.filter_by(email=email).first()
    if not user or not user.verify_password_hash(password):
        if len(email)==0:
            raise Unauthorized("No email provided")
        elif len(password)==0:
            raise Unauthorized("No password provided")
        elif not re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)",
                            email):
            raise Unauthorized("Please provide a valid email")
        else:
            raise Unauthorized("Wrong email and password combination")
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
        email = data.get('email')
        password = data.get('password')
        if email.strip() == "" or password.strip() == "":
            raise BadRequest("Please enter all details")
        elif len(password)<8:
            raise BadRequest("Password should be at least 8 characters long")
        elif not re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)",
                            email):
            raise BadRequest("Please provide a valid email")
        if User.query.filter_by(email=data.get('email')).first() is not None :
            raise BadRequest("User with that email exists")
        create_user(data)
        return 201

@namespace.route('/login')
class LoginUserResource(Resource):
    @aut.login_required
    @api.expect(user)
    def post(self):
        """
        Log in a user

        """
        token = g.user.generate_auth_token()
        return jsonify({'Authorization': token.decode('ascii')})
