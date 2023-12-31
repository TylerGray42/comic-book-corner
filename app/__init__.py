from flask import Flask
from app.routes import get_blueprints


app = Flask(__name__)


for blueprint in get_blueprints():
    app.register_blueprint(blueprint)
