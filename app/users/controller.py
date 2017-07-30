from app.users.models import User
from app import db


def create_user(data):
    email = data.get('email')
    password = data.get('password')

    if email == "" or password == "":
        return "Please enter all details"
    if len(password)<8:
        return "Password should be at least 8 characters long"


    if User.query.filter_by(email=email).first() is not None:
        return "User with that email exists"

    user = User(email=email)

    user.generate_hash(password)
    db.session.add(user)
    db.session.commit()
