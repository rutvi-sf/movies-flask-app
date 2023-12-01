from flask_jwt_extended import create_access_token, create_refresh_token
from flask_mail import Message
from flask_restful import Resource, abort

from api.models import User
from api.serializers import LogInSerializer, SignInSerializer, UserSerializer
from api.utils.decorators import dump_request, load_request
from tasks import send_confirmation_email


class SignUpResource(Resource):
    """
    API Resource to Sign up
    Allowed Verbs: POST
    Request Payload:{
        "full_name": "John Doe",
        "email_id": "john.doe@gmail.com",
        "password": "Test@123",
        "role": "USER"
    }

    Response Object: "Signed Up"
    """

    @load_request(UserSerializer())
    def post(self, serialized_payload: dict):
        user = User.create(**serialized_payload)
        send_confirmation_email(user)
        return "Signed Up", 201



class SignInResource(Resource):
    """
    API Resource to Login
    Allowed Verbs: POST
    Request Payload:{
        "email_id": "john.doe@gmail.com",
        "password": "Test@123"
    }

    Response Object:{
        "access_token": "<jwt-token>",
        "refresh_token": "<jwt-token>",
        "user_obj": {
            "id": "e8e410bb-3e31-415c-8517-23feee1e643d",
            "full_name": "John Doe",
            "email_id": "john.doe@gmail.com",
            "role": "USER"
        }
    }
    """

    @load_request(SignInSerializer())
    @dump_request(LogInSerializer())
    def post(self, serialized_payload: dict):
        # Fetch User from DB if exists else respond 404
        user = User.query.filter(
            User.email_id == serialized_payload["email_id"]
        ).first() or abort(404, message="User Not found")

        # If incorrect password respond 400
        if not user.check_password(serialized_payload["password"]):
            abort(400, message="Incorrect Password")

        # If correct password generate access tokens
        access_token = create_access_token(identity=user)
        refresh_token = create_refresh_token(identity=user)

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "user_obj": user,
        }
