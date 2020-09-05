import logging

from flask import request

from wallet.api import api
from wallet.decorators import check_login, validate

from wallet.schemas.transaction import Transaction as TransactionRequest
from wallet.services.transaction import fetch_transactions, send_transaction

logger = logging.getLogger(__name__)


@api.route('/transaction', methods=['GET'])
@check_login
def get_transactions():
    """
    Fetches transactions for current user

    :return: JSON containing sent and received transactions
    """
    logger.info(f'Getting transactions for user {request.user.id}')
    return fetch_transactions().to_primitive()


@api.route('/transaction', methods=['POST'])
@validate(model=TransactionRequest)
@check_login
def create_transaction(model):
    """
    Creates transaction for current user.

    :param model: Request model
    :return: Created transaction
    """
    logger.info(f'Creating transaction for user {request.user.id}')
    return send_transaction(model)
