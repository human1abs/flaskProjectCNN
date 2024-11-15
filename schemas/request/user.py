from marshmallow import Schema, fields, validates_schema
from schemas.bases import BaseUserSchema
from marshmallow.validate import ValidationError


class RequestRegisterUserSchema(BaseUserSchema):
    pass


class RequestLoginUserSchema(BaseUserSchema):
    pass


class PasswordChangeSchema(Schema):
    old_password = fields.String(required=True)
    new_password = fields.String(required=True)

    @validates_schema
    def validate_passwords(self, data, **kwargs):
        if data["old_password"] == data["new_password"]:
            raise ValidationError(
                "New password cannot be the same as the old password.",
                field_names=["new_password"],
            )

