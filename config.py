import os


class Config(object):

    DEBUG = False
    TESTING = False
    SECRET_KEY = os.environ.get('SECRET_KEY')

    SQLALCHEMY_DATABASE_URI="sqlite:///db.sqlite"

    SESSION_COOKIE_SECURE = True

class ProductionConfig(Config):
    pass


class DevelopmentConfig(Config):

    DEBUG = True

    SQLALCHEMY_DATABASE_URI="sqlite:///db.sqlite"
    SESSION_COOKIE_SECURE = False


class  TestingConfig(Config):

    TESTING = True

    SQLALCHEMY_DATABASE_URI="sqlite:///db.sqlite"
    SESSION_COOKIE_SECURE = False
