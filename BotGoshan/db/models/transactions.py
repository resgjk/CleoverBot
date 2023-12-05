import datetime

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey
from db.database import Base


class TransactionModel(Base):
    __tablename__ = "transactions"

    id: Mapped[int] = mapped_column(
        primary_key=True, nullable=False, autoincrement=True
    )
    uuid: Mapped[str] = mapped_column(nullable=False, unique=True)
    category: Mapped[int] = mapped_column(ForeignKey("categories.id"), nullable=False)
    user: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    date: Mapped[datetime.datetime] = mapped_column(
        nullable=False, default=datetime.datetime.now()
    )

    def __repr__(self) -> str:
        return f"{self.id} {self.uuid} {self.category} {self.user} {self.date}"
