from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS,cross_origin
from .utils import api
from config import app_config




db = SQLAlchemy()

from bucketlists.views import namespace as bucketlist_namespace
from users.views import namespace as auth_namespace


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(app_config[config_name])
    CORS(app)
    db.init_app(app)
    api.init_app(app)
    api.add_namespace(bucketlist_namespace)
    api.add_namespace(auth_namespace)
    return app
