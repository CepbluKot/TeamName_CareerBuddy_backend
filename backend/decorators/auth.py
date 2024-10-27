from functools import wraps
from flask_jwt_extended import get_jwt_identity

from http import HTTPStatus


def role_required(allowed_roles: list):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if not allowed_roles or allowed_roles == ["*"]:
                return func(*args, **kwargs)

            employee_data = get_jwt_identity()
            employee_role = employee_data.get("role")

            if employee_role not in allowed_roles:
                # Redirect or return a 403 Forbidden response if the role is not allowed
                return {
                    "code": 1,
                    "message": "role not allowed",
                }, HTTPStatus.BAD_REQUEST

            return func(*args, **kwargs)

        return wrapper

    return decorator
