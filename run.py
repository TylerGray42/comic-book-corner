from app import app
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt


if __name__ == '__main__':

    app.config.from_object('config.Config')

    login_manager = LoginManager()
    login_manager.session_protection = "strong"
    login_manager.login_view = "login"
    login_manager.login_message_category = "info"

    db = SQLAlchemy()
    bcrypt = Bcrypt()

    login_manager.init_app(app)
    db.init_app(app)
    bcrypt.init_app(app)


    app.run()