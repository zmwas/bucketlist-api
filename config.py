class Config(object):
    DEBUG = False



class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_ECHO = True

class ProductionConfig(Config):
    pass


app_config = {
    'development':DevelopmentConfig,
    'production':ProductionConfig

}
