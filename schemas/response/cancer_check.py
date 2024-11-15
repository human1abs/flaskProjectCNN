from marshmallow import Schema, fields
from marshmallow_enum import EnumField

from models.enums import State


class ResponseCancerSchema(Schema):
    id = fields.Integer(required=True)
    result = fields.String(required=True)
    status = EnumField(State, by_value=True)
    description = fields.String(required=True)
    photo_url = fields.URL(required=True)