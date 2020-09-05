import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from wallet.db import db


class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(UUID, primary_key=True, default=str(uuid.uuid4()), unique=True, nullable=False)
    username = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String)
    balance = relationship("Balance", uselist=False, back_populates="user", primaryjoin='User.id==Balance.user_id')
    transaction = relationship("Transaction", primaryjoin='User.id==Transaction.sender')

    @staticmethod
    def get_by_username(username):
        """
        Gets user by username

        :param username: username to find
        :return: User object
        """
        return User.query.filter_by(username=username).first()

    @staticmethod
    def get_user_by_id(user_id):
        """
         Gets user by id

         :param user_id: user id to find
         :return: User object
         """
        return User.query.filter_by(id=user_id).first()
