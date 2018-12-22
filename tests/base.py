import unittest
import warnings

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from app import conf, db

# https://github.com/marshmallow-code/flask-marshmallow/issues/53
with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    from flask_marshmallow import Marshmallow


class Base(unittest.TestCase):
    db = None

    @classmethod
    def setUpClass(cls):
        super(Base, cls).setUpClass()

        cls.app = cls.create_test_app()
        cls.db.app = cls.app
        cls.db.create_all()

    @classmethod
    def tearDownClass(cls):
        cls.db.drop_all()
        super(Base, cls).tearDownClass()

    def setUp(self):
        super(Base, self).setUp()

        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()

        for table in reversed(db.metadata.sorted_tables):
            db.session.execute(table.delete())

    def tearDown(self):
        self.db.session.rollback()
        self.app_context.pop()

        super(Base, self).tearDown()

    @classmethod
    def create_test_app(cls):
        from app.routes import register_routes

        application = Flask(__name__)
        application.config.from_object(conf.TestConfig)
        cls.db = SQLAlchemy(application)
        Marshmallow(application)
        register_routes(application)

        return application
