from flask_testing import TestCase

from config import create_app
from db import db
from managers.auth import AuthManager
from models import UserModel


def generate_token(user):
    return AuthManager.encode_token(user)


def mock_uuid():
    return "11111111-1111-1111-1111-111111111111"


class APIBaseTestCase(TestCase):
    def create_app(self):
        return create_app("config.TestingConfig")

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def register_user(self):
        data = {
            "email": "c@a.com",
            "password": "csd",
        }

        users = UserModel.query.all()
        self.assertEqual(len(users), 0)

        resp = self.client.post("/register", json=data)
        self.assertEqual(resp.status_code, 201)
        token = resp.json["token"]
        self.assertIsNotNone(data)

        return (data["email"], data["password"])