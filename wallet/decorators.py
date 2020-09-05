import json
import base64
import functools

from werkzeug.security import check_password_hash

from flask import request

from wallet.errors import UnauthorizedError
from wallet.db.user import User

def validate(model, *args, **kwargs):
    """
    Decorator for validating model given as an argument
    :param model: Model to be validated
    :return: Function
    """
    def decorator(func, *args, **kwargs):
        @functools.wraps(func)
        def validate_model(*args, **kwargs):
            data = request.get_json(force=True)
            kwargs['model'] = model(data)
            return func(*args, **kwargs)
        return validate_model
    return decorator


def check_login(func, *args, **kwargs):
    """
       Check if session ID is valid and attaches current user to request
    """
    @functools.wraps(func)
    def auth(*args, **kwargs):
        session = request.headers['session_id']
        session_data = json.loads(base64.b64decode(session))
        user = User.get_by_username(session_data['username'])
        if not user or not check_password_hash(user.password, session_data['password']):
            raise UnauthorizedError()
        request.user = user
        return func(*args, **kwargs)
    return auth
