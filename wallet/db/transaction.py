import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from wallet.db import db


class Transaction(db.Model):
    __tablename__ = 'transaction'

    id = db.Column(UUID, primary_key=True, default=str(uuid.uuid4()), unique=True, nullable=False)
    sender = db.Column(UUID, db.ForeignKey('user.id'))
    sender_id = relationship("User", back_populates="transaction")
    receiver = db.Column(UUID)
    amount = db.Column(db.Numeric(10, 2))

    @staticmethod
    def create_transaction(sender, receiver, amount):
        """
        Creates transaction for given sender and receiver for a given amount

        :param sender: Transaction sender
        :param receiver: Transaction receiver
        :param amount: Amount to be updated
        :return: Transaction object
        """
        transaction = Transaction(
            id=str(uuid.uuid4()),
            sender=sender,
            receiver=receiver,
            amount=amount
        )
        db.session.add(transaction)
        return transaction

    @staticmethod
    def get_transaction_for_sender(user):
        """
        Gets transaction for given sender

        :param user: sender user
        :return: Transaction objects
        """
        return Transaction.query.filter_by(sender=user.id).all()

    @staticmethod
    def get_transaction_for_receiver(user):
        """
        Gets transaction for given receiver

        :param user: Sender user
        :return: Transaction objects
        """
        return Transaction.query.filter_by(receiver=user.id).all()

