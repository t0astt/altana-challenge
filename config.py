import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    """
    Class to provide easy configuration for the application
    """
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL") \
                              or f"sqlite:///{os.path.join(basedir, 'data.sqlite')}"
