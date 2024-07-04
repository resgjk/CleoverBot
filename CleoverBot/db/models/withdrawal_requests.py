from db.base import Base
from db.models.users import UserModel

from datetime import datetime

from sqlalchemy import ForeignKey, DateTime
from sqlalchemy.orm import relationship, mapped_column, Mapped


class WithdrawRequestModel(Base):
    __tablename__ = "withdrawal_requests"

    id: Mapped[int] = mapped_column(
        primary_key=True, unique=True, nullable=False, autoincrement=True
    )
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    user = relationship("UserModel")
    uuid: Mapped[str] = mapped_column(nullable=False, unique=True)
    create_datetime: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
    wallet_address: Mapped[str] = mapped_column(nullable=False, unique=False)
    amount: Mapped[float] = mapped_column(nullable=False, unique=False)
    is_paid: Mapped[bool] = mapped_column(nullable=False, unique=False, default=False)

    def __repr__(self) -> str:
        return f"{self.id} {self.uuid} {self.user_id}"
