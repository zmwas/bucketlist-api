import re
from app.users.models import User
from app import db


def create_user(data):
    """
    Create a user

    """
    email = data.get('email').strip()
    password = data.get('password').strip()

    if email == "" or password == "":
        return "Please enter all details"
    if not re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)",
                        email):
        return "Please provide a valid email"
    if len(password)<8:
        return "Password should be at least 8 characters long"


    if User.query.filter_by(email=email).first() is not None:
        return "User with that email exists"

    user = User(email=email)

    user.generate_hash(password)
    db.session.add(user)
    db.session.commit()
