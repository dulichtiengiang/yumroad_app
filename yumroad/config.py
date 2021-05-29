import os

class BaseConfig:
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///dev.db'
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_ECHO = True

class ProdConfig(BaseConfig):
    pass

class TestConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'
    WTF_CSRF_ENABLED = False


configuration = {
    'dev': DevConfig,
    'test': TestConfig,
    'prod': ProdConfig
}