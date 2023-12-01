import uuid

import bcrypt
from flask_restful import abort
from sqlalchemy import Enum as SQLAlchemyENUM
from sqlalchemy import String
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import mapped_column

from api import db
from api.models.constant import UserRoles


class User(db.Model):
    """
    DB Model for Users
    """

    id = mapped_column(String(36), primary_key=True, default=uuid.uuid4)
    full_name = mapped_column(String(200), nullable=False, index=True)
    email_id = mapped_column(String(200), nullable=False, unique=True)
    password = mapped_column(String(256), nullable=False)
    role = mapped_column(
        SQLAlchemyENUM(UserRoles), nullable=False, default=UserRoles.USER.name
    )

    def __init__(self, *args, **kwargs) -> None:
        super(User, self).__init__(*args, **kwargs)
        self.hash_password()

    def hash_password(self) -> None:
        # Hash the password of the user obj
        self.password = bcrypt.hashpw(self.password.encode("utf-8"), bcrypt.gensalt())

    def check_password(self, password: str) -> bool:
        # Verify Password of the user obj
        return bcrypt.checkpw(password.encode("utf-8"), self.password.encode("utf-8"))

    @staticmethod
    def create(*args, **kwargs) -> "User":
        try:
            user = User(**kwargs)
            db.session.add(user)
            db.session.commit()
            return user
        except IntegrityError as er:
            abort(400, message=f"User already exists {er}")
