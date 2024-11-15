from flask_restful import Resource

from managers.auth import auth
from managers.user import AdminManager
from models import RoleType
from schemas.response.user import ResponseUserSchema
from utils.decorators import permission_required


class GetUser(Resource):
    @auth.login_required
    @permission_required(RoleType.admin)
    def get(self, pk):

        user = AdminManager.get_user(pk)
        return ResponseUserSchema().dump(user)


class DeleteUser(Resource):
    @auth.login_required
    @permission_required(RoleType.admin)
    def delete(self, pk):

        AdminManager.delete_user(pk)
        return 200
