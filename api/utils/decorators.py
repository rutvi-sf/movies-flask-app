from flask import request
from flask_jwt_extended import current_user, jwt_required
from flask_restful import abort


def load_request(serializer):
    """
    A decorator that can be used in service functions to do the validation checks
    of the payload based on provided marshmallow serializer.

    This decorator will pass one extra keyword argument in the service function
    called `serialized_payload`.

    Usage:
        class CreateMovies(Resource):

            @load_request(Moviesserializer())
            def post(self, serialized_payload):
                ...
    """

    def outer_wrapper(service_function, *args, **kwargs):
        def wrapper(*args, **kwargs):
            errors = serializer.validate(request.json)
            if errors:
                abort(400, message=errors)
            serialized_payload = serializer.load(request.json)
            kwargs["serialized_payload"] = serialized_payload

            return service_function(*args, **kwargs)

        return wrapper

    return outer_wrapper


def dump_request(serializer):
    """
    A decorator that can be used in service functions to response into json serializable responses
    using the specified marshmallow serializer.

    Usage:
        class CreateMovies(Resource):

            @dump_request(Moviesserializer())
            def post(self, serialized_payload):
                ...
                return response
    """

    def outer_wrapper(service_function, *args, **kwargs):
        def wrapper(*args, **kwargs):
            response = service_function(*args, **kwargs)
            return serializer.dump(response)

        return wrapper

    return outer_wrapper


def allow_only_roles(allowed_roles):
    """
    A decorator that can be used to decorate service functions to ensure
    that the current user is authenticated and has one of the allowed_roles.

    Usage:
        class CreateMovies(Resource):

            @allow_only_roles([UserRole.ADMIN, UserRole.User])
            def post(self, serialized_payload):
                ...
                return response
    """

    def outer_wrapper(service_function):
        @jwt_required(optional=True)
        def wrapper(*args, **kwargs):
            if not current_user:
                abort(401, message="Unauthenticated User")

            if current_user.role not in allowed_roles:
                abort(403, message="This role is Unauthorized")

            return service_function(*args, **kwargs)

        return wrapper

    return outer_wrapper
