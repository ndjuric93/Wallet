import unittest
from unittest import mock


from wallet.schemas.transaction import Transaction
from wallet.services.transaction import send_transaction
from wallet.errors import (
    NotEnoughFundsError,
    ImpossibleTransaction,
    UnauthorizedError,
    ReceiverDoesNotExist
)


class TransactionService(unittest.TestCase):

    @mock.patch(
        'wallet.services.transaction.request',
        mock.MagicMock(
            user=mock.MagicMock(balance=mock.MagicMock(amount=200))
        )
    )
    @mock.patch(
        'wallet.db.user.User.get_by_username', return_value=mock.MagicMock(
            user=mock.MagicMock(balance=mock.MagicMock(amount=200))
        )
    )
    @mock.patch(
        'wallet.db.transaction.Transaction.create_transaction', return_value=Transaction({
            'amount': 100,
            'receiver': 'SomeUser'
        })
    )
    def testSuccessfulTransaction(self, user, transaction):
        # prepare
        transaction = Transaction({
            'amount': 100,
            'receiver': 'SomeUser'
        })

        # test
        sent_transaction = send_transaction(transaction)
        # assert
        assert transaction.to_primitive() == sent_transaction

    @mock.patch('wallet.services.transaction.request', mock.MagicMock())
    @mock.patch('wallet.db.user.User.get_by_username', return_value=None)
    def testNonExistingReceiver(self, user):
        # prepare

        transaction = Transaction({
            'amount': 100,
            'receiver': 'SomeUser'
        })

        # test
        with self.assertRaises(ReceiverDoesNotExist):
            sent_transaction = send_transaction(transaction)
            # assert
            assert transaction == sent_transaction

    @mock.patch(
        'wallet.services.transaction.request',
        mock.MagicMock(
            user=mock.MagicMock(balance=mock.MagicMock(amount=0))
        )
    )
    @mock.patch('wallet.db.user.User.get_by_username', return_value=mock.MagicMock())
    def testNotEnoughFunds(self, receiver_user):
        # prepare
        transaction = Transaction({
            'amount': 100,
            'receiver': 'SomeUser'
        })

        # test
        with self.assertRaises(NotEnoughFundsError):
            sent_transaction = send_transaction(transaction)
            # assert
            assert transaction == sent_transaction
