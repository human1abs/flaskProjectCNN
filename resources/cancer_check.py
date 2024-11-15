from flask import request
from flask_restful import Resource
from werkzeug.exceptions import NotFound

from managers.auth import auth
from managers.cancer_check import CancerCheckManager
from models.enums import RoleType
from schemas.request.cancer_check import RequestCancerSchema
from schemas.response.cancer_check import ResponseCancerSchema
from utils.decorators import permission_required, validate_schema


class CancerCheck(Resource):

    @auth.login_required
    def get(self):
        user = auth.current_user()
        checks = CancerCheckManager.get_all_cancer_checks_by_user(user)
        return ResponseCancerSchema().dump(checks, many=True)

    @auth.login_required
    @permission_required(RoleType.user)
    @validate_schema(RequestCancerSchema)
    def post(self):
        user = auth.current_user()
        data = request.get_json()
        check = CancerCheckManager.create(data, user)

        return ResponseCancerSchema().dump(check)


class DeleteOwnCheck(Resource):
    @auth.login_required
    @permission_required(RoleType.user)
    def delete(self, pk):
        user = auth.current_user()
        checks = CancerCheckManager.get_all_cancer_checks_by_user(user)
        print(checks)

        for check in checks:
            if pk == check.id:
                CancerCheckManager.delete(pk)
                return 200, {"message": f"Check with id {pk} was successfully deleted"}

        raise NotFound

class MalignantChecks(Resource):
    @auth.login_required
    @permission_required(RoleType.admin)
    def put(self, pk):

        CancerCheckManager.malignant(pk)
        return 204


class UnclearChecks(Resource):
    @auth.login_required
    @permission_required(RoleType.admin)
    def put(self, pk):
        CancerCheckManager.unclear(pk)
        return 204


class BenignChecks(Resource):
    @auth.login_required
    @permission_required(RoleType.admin)
    def put(self, pk):
        CancerCheckManager.benign(pk)
        return 204
