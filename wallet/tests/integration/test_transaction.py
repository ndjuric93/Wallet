import uuid
import unittest

from werkzeug.security import generate_password_hash

from wallet.db import User, Balance
from wallet.db import db
from wallet.main import create_app
from wallet.tests.integration.utils import create_session

from config import TestConfig


class TransactionTest(unittest.TestCase):

    TEST_USERNAME1 = 'username1'
    TEST_USERNAME2 = 'username2'
    TEST_PASSWORD = 'SomePassword'

    @classmethod
    def setUpClass(cls):
        cls.app = create_app(TestConfig)
        cls.app.test_request_context().push()
        db.create_all()
        user1 = User(
            id=str(uuid.uuid4()),
            username=cls.TEST_USERNAME1,
            password=generate_password_hash(cls.TEST_PASSWORD)
        )
        user2 = User(
            id=str(uuid.uuid4()),
            username=cls.TEST_USERNAME2,
            password=generate_password_hash(cls.TEST_PASSWORD)
        )
        balance1 = Balance(
            id=str(uuid.uuid4()),
            user=user1,
            amount=1000
        )
        balance2 = Balance(
            id=str(uuid.uuid4()),
            user=user2,
            amount=1000
        )
        db.session.add(user1)
        db.session.add(user2)
        db.session.add(balance1)
        db.session.add(balance2)
        db.session.commit()

    @classmethod
    def tearDownClass(cls) -> None:
        db.close_all_sessions()
        db.drop_all()

    def setUp(self) -> None:
        self.session_id_user_1 = create_session(
            self.app,
            self.TEST_USERNAME1,
            self.TEST_PASSWORD
        )
        self.session_id_user_2 = create_session(
            self.app,
            self.TEST_USERNAME2,
            self.TEST_PASSWORD
        )

    def test_sending_transaction_non_existing_person(self):
        with self.app.test_client() as client:
            response = client.post(
                '/transaction',
                headers={
                    'session_id': self.session_id_user_1
                },
                json={
                    'receiver': 'DOES_NOT_EXIST',
                    'amount': 100
                }
            )
            assert response.status_code == 400

    def test_sending_transaction_no_funds(self):
        with self.app.test_client() as client:
            response = client.post(
                '/transaction',
                headers={
                    'session_id': self.session_id_user_1
                },
                json={
                    'receiver': self.TEST_USERNAME2,
                    'amount': 10000
                }
            )
            assert response.status_code == 400

    def test_sending_transaction(self):
        with self.app.test_client() as client:
            response = client.post(
                '/transaction',
                headers={
                    'session_id': self.session_id_user_1
                },
                json={
                    'receiver': self.TEST_USERNAME2,
                    'amount': 500
                }
            )
            assert response.status_code == 200
