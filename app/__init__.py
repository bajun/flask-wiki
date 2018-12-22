import warnings

from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from app import conf

# https://github.com/marshmallow-code/flask-marshmallow/issues/53
with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    from flask_marshmallow import Marshmallow

application = Flask(__name__)
application.config.from_object(conf.BaseConfig)
db = SQLAlchemy(application)
migrate = Migrate(application, db)
ma = Marshmallow(application)

from .models import Content, Page, Revision

from .routes import register_routes

register_routes(application)
