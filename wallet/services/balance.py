import logging

from flask import request

from wallet.db.balance import Balance
from wallet.schemas.balance import Balance as BalanceSchema

logger = logging.getLogger(__name__)


def fetch_balance_for_user():
    """
    Gets balance for current user.

    :return: Current balance of the user
    """
    balance = Balance.get_balance_for_user(request.user)
    logger.info(f'Balance fetched successfuly for {request.user.username}')
    return BalanceSchema({'amount': balance.amount})
