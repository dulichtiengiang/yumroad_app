import os

class BaseConfig:
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///dev.db'
    SQLALCHEMY_ECHO = True

class ProdConfig(BaseConfig):
    pass

class TestConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'


configuration = {
    'dev': DevConfig,
    'test': TestConfig,
    'prod': ProdConfig
}