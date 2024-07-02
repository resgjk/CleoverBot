from db.base import Base
from db.models.users import UserModel

from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, mapped_column, Mapped


class AgencyStatModel(Base):
    __tablename__ = "agency_stats"

    id: Mapped[int] = mapped_column(
        primary_key=True, unique=True, nullable=False, autoincrement=True
    )
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    user = relationship("UserModel")
    transaction_id: Mapped[int] = mapped_column(
        ForeignKey("transactions.id"), nullable=False
    )
    transaction = relationship("TransactionModel")
    payment_datetime: Mapped[datetime] = mapped_column(nullable=False)

    def __repr__(self) -> str:
        return f"{self.id} {self.user_id} {self.transaction_id}"
