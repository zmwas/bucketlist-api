import os
basedir = os.path.abspath(os.path.dirname(__file__))
class Config(object):
    ERROR_404_HELP = False
    SECRET_KEY = os.getenv('SECRET')
    pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_ECHO = True

class ProductionConfig(Config):
    DEBUG = False
    SECRET_KEY = os.getenv('SECRET')
    SQLALCHEMY_DATABASE_URI = os.getenv('DB')

class TestingConfig(Config):

    DEBUG = False
    TESTING = True
    WTF_CSRF_ENABLED =False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.getenv('TEST_DB')

app_config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig
}
