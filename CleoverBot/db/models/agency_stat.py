from typing import Literal

from db.base import Base

from datetime import date

from sqlalchemy import BIGINT
from sqlalchemy.orm import relationship, mapped_column, Mapped


class UserModel(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        primary_key=True, unique=True, nullable=False, autoincrement=True
    )

    def __repr__(self) -> str:
        return f"{self.id}"
