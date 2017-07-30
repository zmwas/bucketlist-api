from app import db
from passlib.apps import custom_app_context


class User(db.Model):
    __tablename__  = 'users'
    id = db.Column(db.Integer(),primary_key=True)
    email = db.Column(db.String(64),unique=True)
    password_hash = db.Column(db.String(128))

    def generate_hash(self,password):
        self.password_hash = custom_app_context.encrypt(password)

    def verify_password_hash(self,password):
        return custom_app_context.verify(password,self.password_hash)
