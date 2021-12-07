import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    """
    Class to provide easy configuration for the application
    """
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True

    # [DB_TYPE]+[DB_CONNECTOR]://[USERNAME]:[PASSWORD]@[HOST]:[PORT]/[DB_NAME]
    # https://docs.sqlalchemy.org/en/14/dialects/mysql.html#module-sqlalchemy.dialects.mysql.pymysql
    SQLALCHEMY_DATABASE_URI = f"mariadb+pymysql://altana:password@database:3306/altana"
    # SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL") \
    #                           or f"sqlite:///{os.path.join(basedir, 'data.sqlite')}"
