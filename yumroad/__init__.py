from flask import Flask

from yumroad.config import configuration
from yumroad.extensions import db, csrf, login_manager

from yumroad.blueprints.products import bp_products
from yumroad.blueprints.users import bp_user

def create_app(environment_name='dev'):
    app = Flask(__name__)

    app.config.from_object(configuration[environment_name])
    db .init_app(app)
    csrf.init_app(app)
    login_manager.init_app(app)
    
    app.register_blueprint(bp_products, url_prefix='/product')
    app.register_blueprint(bp_user)

    return app
