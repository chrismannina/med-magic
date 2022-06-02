from flask import Flask
from config import Config


def init_app():
    """Initialize the core app"""
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object('config.Config')

    with app.app_context():
        from . import routes

        return app
