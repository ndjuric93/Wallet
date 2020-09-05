import logging

from wallet.decorators import validate
from wallet.schemas.user import LoginRequest
from wallet.api import api
from wallet.services.login import login_user


logger = logging.getLogger(__name__)


@api.route('/login', methods=['POST'])
@validate(model=LoginRequest)
def login(model):
    """
    Login for the user.

    :param model: Login request
    :return: Session ID for the user
    """
    logger.info(f'User {model.username} logging')
    session = login_user(model)
    return {
        'session': session
    }
