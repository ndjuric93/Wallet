import uuid

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from wallet.db import db


class Balance(db.Model):
    __tablename__ = 'balance'

    id = db.Column(UUID, primary_key=True, default=str(uuid.uuid4()), unique=True, nullable=False)
    user_id = db.Column(UUID, db.ForeignKey('user.id'))
    user = relationship("User", back_populates="balance", foreign_keys=[user_id])
    amount = db.Column(db.Numeric(10, 2))

    @staticmethod
    def get_balance_for_user(user):
        """
        Fetches balance from DB for given user.

        :param user: User to fetch balance for
        :return: Balance object for the user
        """
        return Balance.query.filter_by(user_id=user.id).first()

    def update_balance(self, amount):
        """
        Updates balance by given amount

        :param amount: Amount to be updated
        :return: Balance object
        """
        self.amount += amount
        db.session.add(self)
        return self
