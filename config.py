class Config(object):
    SECRET_KEY = 'nqqijvwyv+8@kwag_9k^&2gnvw40qf34^=l$s6ph#3vnug4f)'




class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_ECHO = True

class ProductionConfig(Config):
    pass



class TestingConfig(Config):
    DEBUG = False
    TESTING = True
    WTF_CSRF_ENABLED =False
    SQLALCHEMY_DATABASE_URI = 'postgresql://localhost/test_db'

app_config = {
    'development':DevelopmentConfig,
    'production':ProductionConfig,
    'testing' :TestingConfig

}
