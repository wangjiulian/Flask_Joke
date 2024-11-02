from flask import Flask
from .config import Config
from .routes.joke_route import joke
from .db import init_app


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    init_app(app)

    app.register_blueprint(joke)

    return app
