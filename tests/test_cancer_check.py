import json
import os
from unittest.mock import patch

from flask_testing import TestCase

from config import create_app
from constants import TEMP_FILE_FOLDER
from db import db
from models import CancerCheckModel
from services.s3 import S3Service
from tests.base import generate_token, mock_uuid
from tests.factories import UserFactory
from tests.helpers import encoded_file


class TestCancerCheck(TestCase):
    url = "/user/checks"

    def create_app(self):
        return create_app("config.TestingConfig")

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_cancer_check_missing_input_fields_raises(self):
        user = UserFactory()
        token = generate_token(user)

        checks = CancerCheckModel.query.all()
        self.assertEqual(len(checks), 0)

        data = {
            "photo": encoded_file,
            "photo_extension": "jpg"
        }

        for key in data:
            current_data = data.copy()
            print(current_data)
            current_data.pop(key)
            resp = self.client.post(
                self.url,
                data= json.dumps(current_data),
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {token}",
                },
            )

            message = resp.json["message"]
            expected_message = (
                "{'" + key + "': ['Missing data for required field.']}"
            )
            self.assert400(resp)
            self.assertEqual(message, expected_message)

        checks = CancerCheckModel.query.all()
        self.assertEqual(len(checks), 0)

    @patch("uuid.uuid4", mock_uuid)
    @patch.object(S3Service, "upload_photo", return_value="some.s3.url")
    def test_cancer_check(self, mocked_upload):
        user = UserFactory()
        token = generate_token(user)

        checks = CancerCheckModel.query.all()
        self.assertEqual(len(checks), 0)

        data = {
            "photo": encoded_file,
            "photo_extension": "jpg",
        }

        resp = self.client.post(
            self.url,
            data=json.dumps(data),
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {token}",
            },
        )

        self.assert200(resp)

        name = f'{user.id}{mock_uuid()}.{data["photo_extension"]}'
        path = os.path.join(TEMP_FILE_FOLDER, name)

        checks = CancerCheckModel.query.all()
        self.assertEqual(len(checks), 1)
        check = checks[0]
        self.assertEqual(check.photo_url, mocked_upload.return_value)

        mocked_upload.assert_called_once_with(
            path, f"{user.id}{mock_uuid()}.{data['photo_extension']}", data["photo_extension"]
        )
