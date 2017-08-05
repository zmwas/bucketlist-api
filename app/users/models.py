import os
import app
from app import db
from passlib.apps import custom_app_context as pwdcontext
from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer,
                          BadSignature,
                          SignatureExpired)



class User(db.Model):
    __tablename__  = 'users'
    id = db.Column(db.Integer(),primary_key=True)
    email = db.Column(db.String(64),unique=True)
    password_hash = db.Column(db.String(128))
    bucketlists = db.relationship('BucketList',backref='user',lazy='dynamic')

    def generate_hash(self,password):
        self.password_hash = pwdcontext.encrypt(password)

    def verify_password_hash(self,password):
        return pwdcontext.verify(password,self.password_hash)

    def generate_auth_token(self,expiration=700):
        serializer = Serializer(os.getenv('SECRET'),expires_in=expiration)
        return serializer.dumps({'id':self.id})

    @staticmethod
    def verify_auth_token(token):

        serializer = Serializer(os.getenv('SECRET'))
        try:
            data = serializer.loads(token)
        except SignatureExpired:
            return SignatureExpired    # valid token, but expired
        except BadSignature:
            return BadSignature    # invalid token
        user = User.query.get(data['id'])
        return user
