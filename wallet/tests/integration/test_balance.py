import unittest

from werkzeug.security import generate_password_hash

from wallet.db import User, Balance
from wallet.db import db
from wallet.main import create_app

from wallet.tests.integration.utils import create_session

from config import TestConfig


class BalanceTest(unittest.TestCase):

    TEST_USERNAME = 'SomeUser'
    TEST_PASSWORD = 'SomePassword'

    @classmethod
    def setUpClass(cls):
        cls.app = create_app(TestConfig)
        cls.app.test_request_context().push()
        db.create_all()
        user = User(
            username=cls.TEST_USERNAME,
            password=generate_password_hash(cls.TEST_PASSWORD)
        )
        db.session.add(user)
        db.session.add(Balance(user=user, amount=1000))
        db.session.commit()

    @classmethod
    def tearDownClass(cls) -> None:
        db.close_all_sessions()
        db.drop_all()

    def setUp(self) -> None:
        self.session_id = create_session(
            self.app,
            self.TEST_USERNAME,
            self.TEST_PASSWORD
        )

    def test_balance_fetch(self):
        with self.app.test_client() as client:
            response = client.get(
                '/balance',
                headers={'session_id': self.session_id}
            )
            assert response.status_code == 200
