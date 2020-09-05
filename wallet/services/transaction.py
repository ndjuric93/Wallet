import logging
from decimal import Decimal

from flask import request


from wallet.errors import NotEnoughFundsError, ReceiverDoesNotExist, ImpossibleTransaction
from wallet.db import User, Transaction
from wallet.schemas.transaction import (
    TransactionList,
    SentTransaction,
    ReceivedTransaction,
)

logger = logging.getLogger(__name__)


def fetch_transactions():
    """
    Fetches all received and sent transactions for current user.

    :return: Dictionary with sent and received transactions
    """
    sender_transactions = Transaction.get_transaction_for_sender(request.user)
    receiver_transactions = Transaction.get_transaction_for_receiver(request.user)
    logger.info(f'Transactions for {request.user.id} fetched successfully')
    return TransactionList(
        {
            'sent': [
                SentTransaction({
                    'amount': transaction.amount,
                    'receiver': User.get_user_by_id(transaction.sender).username
                }).to_native() for transaction in sender_transactions
            ],
            'received': [
                ReceivedTransaction({
                    'amount': transaction.amount,
                    'sender': User.get_user_by_id(transaction.receiver).username
                }).to_native() for transaction in receiver_transactions
            ]
        }
    )


def send_transaction(model):
    """
    Creates transaction for user with given parameters.

    :param model: Transaction request model
    :return: Model of created transaction

    :raises: ImpossibleTransaction if sender and receiver are equal
    :raises: ReceiverDoesNotExist if non existing receiver in model
    :raises: NotEnoughFundsError if sender has not enough funds
    """
    sender = request.user
    receiver = User.get_by_username(model.receiver)
    if sender == receiver:
        raise ImpossibleTransaction()
    if not receiver:
        raise ReceiverDoesNotExist()
    if sender.balance.amount < model.amount:
        raise NotEnoughFundsError()

    sender.balance.update_balance(-Decimal(model.amount))
    receiver.balance.update_balance(Decimal(model.amount))
    Transaction.create_transaction(
        sender=sender.id,
        receiver=receiver.id,
        amount=model.amount
    )
    logger.info(f'Transaction for {request.user.id} created successfully')
    return model.to_primitive()
