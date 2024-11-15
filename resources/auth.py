from flask import request
from flask_restful import Resource

from managers.auth import auth, AuthManager
from managers.user import UserManager
from models.enums import RoleType
from schemas.request.user import RequestLoginUserSchema, RequestRegisterUserSchema, PasswordChangeSchema
from utils.decorators import validate_schema, permission_required


class Register(Resource):
    @validate_schema(RequestRegisterUserSchema)
    def post(self):
        data = request.get_json()
        token = UserManager.register(data)
        return {"token": token}, 201


class Login(Resource):
    @validate_schema(RequestLoginUserSchema)
    def post(self):
        data = request.get_json()
        token = UserManager.login(data)
        return {"token": token}, 201


class DeleteOwnAccount(Resource):
    @auth.login_required
    @permission_required(RoleType.user)
    def delete(self):
        user = auth.current_user()
        UserManager.delete(user.id)
        return 200, "Your account was successfully deleted"


class Password(Resource):
    @auth.login_required
    @validate_schema(PasswordChangeSchema)
    def post(self):
        data = request.get_json()
        AuthManager.change_password(data)
        return 204
