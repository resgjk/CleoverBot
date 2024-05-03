from datetime import datetime, timezone

from db.base import Base

from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, mapped_column, Mapped


class TransactionModel(Base):
    __tablename__ = "transactions"

    id: Mapped[int] = mapped_column(
        primary_key=True, unique=True, nullable=False, autoincrement=True
    )
    uuid: Mapped[str] = mapped_column(nullable=False, unique=True)
    type: Mapped[str] = mapped_column(nullable=False, unique=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    user = relationship("UserModel", back_populates="transactions")
    is_success: Mapped[bool] = mapped_column(
        nullable=False, default=False, unique=False
    )
    date: Mapped[str] = mapped_column(
        nullable=False, default=str(datetime.now(tz=timezone.utc)), unique=False
    )

    def __repr__(self) -> str:
        return f"{self.id} {self.uuid} {self.user} {self.date}"
