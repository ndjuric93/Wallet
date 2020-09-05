import logging

from flask import request

from wallet.api import api
from wallet.decorators import check_login
from wallet.services.balance import fetch_balance_for_user

logger = logging.getLogger(__name__)


@api.route('/balance', methods=['GET'])
@check_login
def get_balance():
    """
    Fetches balance for the current user.

    :return: Current balance for the user
    """
    logger.info(f'Getting balance for user {request.user.id}')
    return fetch_balance_for_user().to_primitive()
