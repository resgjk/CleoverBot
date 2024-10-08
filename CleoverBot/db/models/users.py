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
    user_id: Mapped[int] = mapped_column(BIGINT, unique=True, nullable=False)
    is_subscriber: Mapped[bool] = mapped_column(
        nullable=False, default=False, unique=False
    )
    subscriber_until: Mapped[date] = mapped_column(nullable=True, unique=False)
    bank: Mapped[Literal["Zero bank", "$100 - 1000", "$1000 - 10000", "$10k+"]] = (
        mapped_column(nullable=False, default="Zero bank")
    )
    notification: Mapped[str] = mapped_column(nullable=False, default="1 Hour")
    activities: Mapped[list["ActivityModel"]] = relationship(  # type: ignore
        back_populates="users", secondary="users_to_activities"
    )
    projects: Mapped[list["ProjectModel"]] = relationship(  # type: ignore
        back_populates="users", secondary="users_to_projects"
    )
    transactions: Mapped[list["TransactionModel"]] = relationship(  # type: ignore
        "TransactionModel", back_populates="user", lazy=True
    )

    def __repr__(self) -> str:
        return f"{self.id} {self.user_id} {self.is_subscriber} {self.subscriber_until} {self.bank} {self.notification}"
