import json

from werkzeug.exceptions import HTTPException


class NotEnoughFundsError(HTTPException):
    code = 400
    name = 'Not enough funds'
    description = 'Trying to send too much money'


class UnauthorizedError(HTTPException):
    code = 400
    name = 'Unauthorized exception'
    description = 'Trying to log in with wrong credentials'


class ReceiverDoesNotExist(HTTPException):
    code = 400
    name = 'Receiver does not exist'
    description = 'Trying to send transaction to non existing user'


class ImpossibleTransaction(HTTPException):
    code = 400
    name = 'Sender and receiver should be different'
    description = 'Trying to send transaction to send money to yourself'


def handle_exception(e):
    """Return JSON instead of HTML for HTTP errors."""
    # start with the correct headers and status code from the error
    response = e.get_response()
    # replace the body with JSON
    response.data = json.dumps({
        "code": e.code,
        "name": e.name,
        "description": e.description,
    })
    response.content_type = "application/json"
    return response
