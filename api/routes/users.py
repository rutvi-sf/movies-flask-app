from api import api
from api.services import SignInResource, SignUpResource


USER_PREFIX = "/users"

api.add_resource(SignUpResource, f"{USER_PREFIX}")
api.add_resource(SignInResource, f"{USER_PREFIX}/sign-in")
