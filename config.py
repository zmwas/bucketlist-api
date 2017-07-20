import os


class Config(object):
    ERROR_404_HELP = False
    pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_ECHO = True

class ProductionConfig(Config):
    pass


class TestingConfig(Config):
    SECRET_KEY = 'nqqijvwyv+8@kwag_9k^&2gnvw40qf34^=l$s6ph#3vnug4f)'

    DEBUG = False
    TESTING = True
    WTF_CSRF_ENABLED =False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = ('sqlite:///' +
                                os.path.join('./', 'bucket_list.db'))

app_config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig
}
