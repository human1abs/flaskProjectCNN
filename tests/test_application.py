from models.enums import RoleType
from models.user import UserModel
from tests.base import APIBaseTestCase
from tests.base import generate_token
from tests.factories import UserFactory


class TestApp(APIBaseTestCase):
    endpoints = (
        ("GET", "user/checks"),
        ("POST", "user/checks"),
        ("DELETE", "user/delete"),
        ("DELETE", "user/checks/10/delete"),
        ("POST", "user/change-password"),
        ("PUT", "admin/checks/1/benign"),
        ("PUT", "admin/checks/1/malignant"),
        ("PUT", "admin/checks/1/unclear"),
        ("GET", "admin/users/1"),
        ("DELETE", "admin/users/1/delete"),
    )

    def make_request(self, method, url, headers=None):
        if method == "GET":
            resp = self.client.get(url, headers=headers)
        elif method == "POST":
            resp = self.client.post(url, headers=headers)
        elif method == "PUT":
            resp = self.client.put(url, headers=headers)
        else:
            resp = self.client.delete(url, headers=headers)

        return resp

    def test_login_required_all_endpoints(self):
        for method, url in self.endpoints:
            resp = self.make_request(method, url)

            self.assertEqual(resp.status_code, 401)
            expected_message = {"message": "Invalid or missing token"}
            self.assertEqual(resp.json, expected_message)

    def test_login_required_endpoints_invalid_token(self):
        headers = {"Authorization": "Bearer invalid"}

        for method, url in self.endpoints:
            resp = self.make_request(method, url, headers=headers)

            self.assertEqual(resp.status_code, 401)
            expected_message = {"message": "Invalid or missing token"}
            self.assertEqual(resp.json, expected_message)

    def test_permission_required_endpoints_admins(self):
        endpoints = (("PUT", "admin/checks/1/benign"),
        ("PUT", "admin/checks/1/malignant"),
        ("PUT", "admin/checks/1/unclear"),
        ("GET", "admin/users/1"),
        ("DELETE", "admin/users/1/delete"),)

        user = UserFactory()
        user_token = generate_token(user)
        headers = {"Authorization": f"Bearer {user_token}"}
        for method, url in endpoints:
            resp = self.make_request(method, url, headers=headers)

            self.assertEqual(resp.status_code, 403)
            expected_message = {
                "message": "You do not have permission to access this resource"
            }
            self.assertEqual(resp.json, expected_message)

    def test_permission_required_endpoints_user(self):
        endpoints = (("POST", "user/checks"),
        ("DELETE", "user/delete"),
        ("DELETE", "user/checks/10/delete"))

        user = UserFactory(role=RoleType.admin)
        user_token = generate_token(user)
        headers = {"Authorization": f"Bearer {user_token}"}
        for method, url in endpoints:
            resp = self.make_request(method, url, headers=headers)

            self.assertEqual(resp.status_code, 403)
            expected_message = {
                "message": "You do not have permission to access this resource"
            }
            self.assertEqual(resp.json, expected_message)


class TestRegister(APIBaseTestCase):
    def test_register_schema_missing_fields(self):
        data = {}

        users = UserModel.query.all()
        self.assertEqual(len(users), 0)

        resp = self.client.post("/register", json=data)
        self.assertEqual(resp.status_code, 400)
        error_message = resp.json["message"]
        for field in ("email", "password"):
            self.assertIn(field, error_message)

        users = UserModel.query.all()

        self.assertEqual(len(users), 0)

    def test_register_schema_invalid_email(self):
        data = {
            "email": "aa.com",
            "password": "asd",
        }

        users = UserModel.query.all()
        self.assertEqual(len(users), 0)

        resp = self.client.post("/register", json=data)
        self.assertEqual(resp.status_code, 400)
        error_message = resp.json["message"]
        expected_message = "{'email': ['Not a valid email address.']}"
        self.assertEqual(error_message, expected_message)

    def test_register(self):
        data = {
            "email": "goshko@gmail.com",
            "password": "csd",
        }

        users = UserModel.query.all()
        self.assertEqual(len(users), 0)

        resp = self.client.post("/register", json=data)
        self.assertEqual(resp.status_code, 201)
        token = resp.json["token"]
        self.assertIsNotNone(token)


class TestLoginSchema(APIBaseTestCase):
    def test_login_schema_missing_fields(self):
        data = {}

        resp = self.client.post("/login", json=data)
        self.assertEqual(resp.status_code, 400)
        error_message = resp.json["message"]
        for field in ("email", "password"):
            self.assertIn(field, error_message)

    def test_login_schema_invalid_email(self):
        email, password = self.register_user()

        data = {
            "email": "asd",
            "password": "asd",
        }

        self.assertNotEqual(email, data["email"])

        resp = self.client.post("/login", json=data)
        self.assertEqual(resp.status_code, 400)
        error_message = resp.json["message"]
        expected_message = "{'email': ['Not a valid email address.']}"
        self.assertEqual(error_message, expected_message)

    def test_login(self):
        email, password = self.register_user()

        data = {
            "email": email,
            "password": password,
        }

        #user = UserFactory(password=data["password"], email=data["email"])

        resp = self.client.post("/login", json=data)
        self.assertEqual(resp.status_code, 201)
        token = resp.json["token"]
        self.assertIsNotNone(token)

    def test_login_invalid_email_raises(self):
        email, password = self.register_user()

        data = {
            "email": "t@a.com",
            "password": password,
        }

        self.assertNotEqual(email, data["email"])

        user = UserModel.query.filter_by(email="t@a.com").all()
        self.assertEqual(len(user), 0)

        resp = self.client.post("/login", json=data)
        self.assertEqual(resp.status_code, 400)
        message = resp.json
        expected_message = {
            "message": "Invalid username or password"
        }
        self.assertEqual(message, expected_message)

    def test_login_invalid_password_raises(self):
        email, password = self.register_user()

        data = {
            "email": email,
            "password": "invalid",
        }
        self.assertNotEqual(password, data["password"])

        user = UserModel.query.filter_by(email="c@a.com").all()
        self.assertEqual(len(user), 1)

        resp = self.client.post("/login", json=data)
        self.assertEqual(resp.status_code, 400)
        message = resp.json
        expected_message = {
            "message": 'Invalid username or password'}

        self.assertEqual(message, expected_message)