from functools import wraps
from flask import request
from flask_restplus import abort

# Secure method decorator
def require_auth(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # Verify if User is Authenticated
        # Authentication logic goes here
        if request.headers.get('authorization'):
            return func(*args, **kwargs)
        else:
            return abort(401)
    return wrapper