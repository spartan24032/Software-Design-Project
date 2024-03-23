import os

class Config(object):
    ENV = 'development'
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.environ.get('SECRET_KEY', default='BAD_SECRET_KEY')
    
class ProductionConfig(Config):
    ENV = 'production'

class DevelopmentConfig(Config):
    ENV = 'development'
    DEBUG = True

class TestingConfig(Config):
    ENV = 'testing'
    TESTING = True
    WTF_CSRF_ENABLED = False
