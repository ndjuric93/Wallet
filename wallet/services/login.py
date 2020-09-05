import logging
import json
import base64

from werkzeug.security import check_password_hash

from wallet.errors import UnauthorizedError
from wallet.db.user import User

logger = logging.getLogger(__name__)


def login_user(login_request):
    """
    Validate login data

    NOTE!!!
    LOGIN IMPLEMENTATION IS SIMPLIFIED AND NOT SAFE.
    AS REQUIREMENTS DIDN'T SPECIFICALLY REQUIRE COMPLEX LOGIN
    SECURED IMPLEMENTATION SUCH AS JWT_TOKEN, SESSIONS THAT EXPIRE ETC.
    IS OMITTED

    :param login_request: Login model to be validated
    :return: Session ID
    """
    user = User.get_by_username(login_request.username)
    if user and check_password_hash(user.password, login_request.password):
        logger.info(f'Login for user: {user.username} successful')
        return base64.b64encode(
            json.dumps(login_request.to_primitive()).encode('utf-8')
        ).decode()
    logger.error(f'Login for user: {login_request.username} failed')
    raise UnauthorizedError()

