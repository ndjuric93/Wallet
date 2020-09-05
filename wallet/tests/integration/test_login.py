import unittest
import uuid

from werkzeug.security import generate_password_hash

from wallet.db import User
from wallet.db import db
from wallet.main import create_app

from config import TestConfig


class LoginTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.app = create_app(TestConfig)
        cls.app.test_request_context().push()
        db.create_all()
        user = User(
            id=str(uuid.uuid4()),
            username='SomeUser',
            password=generate_password_hash('SomePassword'))
        db.session.add(user)
        db.session.commit()

    @classmethod
    def tearDownClass(cls) -> None:
        db.close_all_sessions()
        db.drop_all()

    def test_login_right_credentials(self):
        with self.app.test_client() as client:
            response = client.post(
                '/login',
                json={
                    'username': 'SomeUser',
                    'password': 'SomePassword'
                }
            )
            assert response.status_code == 200
            assert 'session' in response.json

    def test_login_wrong_credentials(self):
            with self.app.test_client() as client:
                response = client.post(
                    '/login',
                    json={
                        'username': 'SomeUser',
                        'password': 'WrongPassword'
                    }
                )
                assert response.status_code == 400
