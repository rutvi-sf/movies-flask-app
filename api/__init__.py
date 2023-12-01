from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy


api = Api()
db = SQLAlchemy()

from api.routes.movies import *  # noqa
from api.routes.users import *  # noqa



__all__ = ["api", "db"]
