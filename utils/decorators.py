from flask import request
from marshmallow import Schema
from werkzeug.exceptions import Forbidden, BadRequest

from managers.auth import auth


def permission_required(role):
    def decorator(function):
        def wrapper(*args, **kwargs):
            user = auth.current_user()
            if user.role != role:
                raise Forbidden("You do not have permission to access this resource")
            return function(*args, **kwargs)
        return wrapper
    return decorator


def validate_schema(schema_name):
    def validation(function):
        def stuff(*args, **kwargs):
            schema: Schema = schema_name()
            data = request.get_json()
            errors = schema.validate(data)
            if errors:
                raise BadRequest(str(errors))

            return function(*args, **kwargs)
        return stuff
    return validation



