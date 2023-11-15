from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt


login_manager = LoginManager()
login_manager.session_protection = "strong"
login_manager.login_view = "login"
login_manager.login_message_category = "info"

db = SQLAlchemy()
bcrypt = Bcrypt()


passF = open(".pass", 'r')
login = passF.readlines()
passF.close()


def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'c9a1e7e34db4eea5c3948a949e4d71208b1460ed01322605'
    app.config["SQLALCHEMY_DATABASE_URI"] = f"mariadb+mariadbconnector://{login[0].strip()}:{login[1].strip()}@127.0.0.1:3306/comicshop"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

    login_manager.init_app(app)
    db.init_app(app)
    bcrypt.init_app(app)
    
    return app