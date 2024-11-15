from sqlalchemy.orm import Mapped, mapped_column

from db import db
from models.enums import RoleType


class UserModel(db.Model):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(db.String(120), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(db.String(255), nullable=False)
    role: Mapped[RoleType] = mapped_column(
        db.Enum(RoleType), default=RoleType.user.name, nullable=False
    )