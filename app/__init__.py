from flask import Flask
from .config import Config
from .routes.joke_route import joke
from .db import init_db
from .routes import init_swagger


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    init_db(app)
    app.register_blueprint(joke)
    init_swagger(app)

    return app
