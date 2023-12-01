from celery import Celery
from flask import Flask
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate

from api import api, db
from api.models import *
from config import DevelopmentConfig, TestingConfig


def create_app(for_testing=False):
    app = Flask(__name__)

    # Load configuration from the Config class
    if for_testing:
        app.config.from_object(TestingConfig)
    else:
        app.config.from_object(DevelopmentConfig)

    api.init_app(app)

    db.init_app(app)
    Migrate(app, db)

    # Initialiazing celery worker
    celery = Celery(app.name, broker=app.config["CELERY_BROKER_URL"])
    celery.conf.update(app.config)

    jwt = JWTManager(app)

    @jwt.user_identity_loader
    def user_identity_lookup(user):
        return user.email_id

    @jwt.user_lookup_loader
    def user_lookup_callback(_jwt_header, jwt_data):
        identity = jwt_data["sub"]
        return User.query.filter_by(email_id=identity).one_or_none()

    return app
