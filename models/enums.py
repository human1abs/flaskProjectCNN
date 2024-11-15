from enum import Enum


class RoleType(Enum):
    user = "user"
    admin = "admin"


class State(Enum):
    benign = "benign"
    unclear = "unclear"
    malignant = "malignant"