import os

class BaseConfig:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_ENABLED = True
    SECRET_KEY = os.getenv('SECRET_KEY', 'rand0102323') #resion need this bc 

class DevConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///dev.db'
    SQLALCHEMY_ECHO = True
    SECRET_KEY = os.getenv('SECRET_KEY', '0e778f7378864bc590a26057872dbcc7')

class TestConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'
    WTF_CSRF_ENABLED = False
    TESTING = True

class ProdConfig(BaseConfig):
    SECRET_KEY = os.getenv('SECRET_KEY')


configuration = {
'dev': DevConfig,
    'test': TestConfig,
    'prod': ProdConfig
}
