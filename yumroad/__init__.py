from flask import Flask

from yumroad.config import configuration
from yumroad.extensions import db

from yumroad.blueprints.product import product as bp_product

def create_app(environment_name='dev'):
    app = Flask(__name__)

    app.config.from_object(configuration[environment_name])
    db .init_app(app)

    app.register_blueprint(bp_product, url_prefix='/product')

    return app
