from flask import Flask

from yumroad.config import configuration
from yumroad.extensions import db

from yumroad.blueprints.products import products as bp_products

def create_app(environment_name='dev'):
    app = Flask(__name__)

    app.config.from_object(configuration[environment_name])
    db .init_app(app)

    app.register_blueprint(bp_products, url_prefix='/product')

    return app
