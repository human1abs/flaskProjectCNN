from datetime import datetime, timedelta

import jwt
from decouple import config
from flask_httpauth import HTTPTokenAuth
from werkzeug.exceptions import Unauthorized, NotFound
from werkzeug.security import check_password_hash, generate_password_hash

from db import db
from models import UserModel


class AuthManager:
    @staticmethod
    def encode_token(user):
        payload = {"sub": user.id, "exp": datetime.utcnow() + timedelta(days=2),
                   "role": user.role if isinstance(user.role, str) else user.role.name}
        return jwt.encode(payload, key=config("SECRET_KEY"), algorithm="HS256")

    @staticmethod
    def decode_token(token):
        try:
            info = jwt.decode(jwt=token, key=config('SECRET_KEY'),  algorithms=["HS256"])
            return info['sub'], info["role"]
        except Exception as ex:
            raise ex

    @staticmethod
    def change_password(pass_data):
        user = auth.current_user()
        if not check_password_hash(user.password, pass_data["old_password"]):
            raise NotFound("Wrong or invalid password")

        new_password_hash = generate_password_hash(
            pass_data["new_password"], method="pbkdf2:sha256"
        )
        db.session.execute(
            db.update(UserModel)
            .where(UserModel.id == user.id)
            .values(password=new_password_hash)
        )


auth = HTTPTokenAuth(scheme='Bearer')


@auth.verify_token
def verify_token(token):
    try:
        user_id, type_user = AuthManager.decode_token(token)
        return db.session.execute(db.select(UserModel).filter_by(id=user_id)).scalar()
    except Exception:
        raise Unauthorized("Invalid or missing token")