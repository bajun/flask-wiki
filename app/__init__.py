from flask import Flask
from flask_marshmallow import Marshmallow

from app import conf
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

application = Flask(__name__)
application.config.from_object(conf.Config)
db = SQLAlchemy(application)
migrate = Migrate(application, db)
ma = Marshmallow(application)

from .models import Content, Page, Revision
from .views import APIListView, PageView, RevisionView
from .routes import *
