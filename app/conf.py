import os


class BaseConfig(object):
    DEBUG = os.environ.get('FLASK_DEBUG', True)
    DB_URL = os.environ.get("FLASK_DB_URL", "localhost")
    DB_PORT = os.environ.get("FLASK_DB_PORT", "5432")
    DB_NAME = os.environ.get("FLASK_DB_NAME", "flaskwiki")
    DB_USER = os.environ.get("FLASK_DB_USER", "wikiadmin")
    DB_PASSWORD = os.environ.get("FLASK_DB_PASSWORD", "12345")
    SQLALCHEMY_DATABASE_URI = \
         f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_URL}:{DB_PORT}/{DB_NAME}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False



class TestConfig(BaseConfig):
    TESTING = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
