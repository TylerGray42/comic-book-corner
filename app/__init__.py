from flask import Flask
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from app.routes import get_blueprints
from config import Config


def create_app(config_class=Config):

    app = Flask(__name__)
    app.config.from_object(config_class)

    login_manager = LoginManager()
    login_manager.session_protection = "strong"
    login_manager.login_view = "login"
    login_manager.login_message_category = "info"

    bcrypt = Bcrypt()

    db = SQLAlchemy()

    login_manager.init_app(app)
    bcrypt.init_app(app)
    db.init_app(app)


    for blueprint in get_blueprints():
        app.register_blueprint(blueprint)

    return app