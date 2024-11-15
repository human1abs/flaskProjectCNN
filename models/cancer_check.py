from datetime import datetime

from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db import db
from models.enums import State
from models.user import UserModel


class CancerCheckModel(db.Model):
    __tablename__ = 'checks'

    id: Mapped[int] = mapped_column(primary_key=True)
    description: Mapped[str] = mapped_column(db.Text, nullable=False)
    photo_url: Mapped[str] = mapped_column(db.String(255), nullable=False)
    result: Mapped[float] = mapped_column(db.String, nullable=False)
    created_on: Mapped[datetime] = mapped_column(db.DateTime, server_default=func.now())
    status: Mapped[State] = mapped_column(
        db.Enum(State),
        default=State.benign,
        nullable=False
    )
    user_id: Mapped[int] = mapped_column(db.Integer, db.ForeignKey('users.id'))
    user: Mapped["UserModel"] = relationship('UserModel')

