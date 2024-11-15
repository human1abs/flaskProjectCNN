from decouple import config
from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from flask_restful import Api

from db import db
from resources.routes import *


class ProductionConfig:
    FLASK_ENV = "prod"
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = (
        f"postgresql://{config('DB_USER')}:{config('DB_PASSWORD')}"
        f"@localhost:{config('DB_PORT')}/{config('DB_NAME')}"
    )


class DevelopmentConfig:
    FLASK_ENV = "development"
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = (
        f"postgresql://{config('DB_USER')}:{config('DB_PASSWORD')}"
        f"@localhost:{config('DB_PORT')}/{config('DB_NAME')}"
    )


class TestingConfig:
    FLASK_ENV = "testing"
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = (
        f"postgresql://{config('TEST_DB_USER')}:{config('TEST_DB_PASSWORD')}"
        f"@localhost:{config('TEST_DB_PORT')}/{config('TEST_DB_NAME')}"
    )


def create_app(environ):
    app = Flask(__name__)
    app.config.from_object(environ)
    db.init_app(app)
    migrate = Migrate(app, db)
    api = Api(app)
    CORS(app)
    [api.add_resource(*route) for route in routes]
    return app
