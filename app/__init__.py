from flask import Flask
from config import Config
# from flask_sqlalchemy import SQLAlchemy
# import psycopg2

# globally accessible libraries
# db = SQLAlchemy()

def init_app():
    """Initialize the core app"""
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object('config.Config')

    # init plugins
    # db.init_app(app)

    with app.app_context():
        # include routes
        from . import routes

        return app