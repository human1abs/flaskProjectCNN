from marshmallow import Schema, fields
from marshmallow_enum import EnumField

from models.enums import State


class RequestCancerSchema(Schema):
    photo = fields.String(required=True)
    photo_extension = fields.String(required=True)
    #description = fields.String(required=True)