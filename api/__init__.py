from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from config import Config

db = SQLAlchemy()


def create_app() -> Flask:
    """
    Application factory for creating the Flask app
    :return: Flask app
    """
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
