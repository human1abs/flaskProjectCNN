from marshmallow import Schema, fields


class BaseUserSchema(Schema):
    email = fields.Email(required=True)
    password = fields.String(required=True)