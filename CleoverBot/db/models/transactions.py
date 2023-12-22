import datetime

from db.base import Base

from sqlalchemy import Column, INTEGER, VARCHAR, BOOLEAN, DATETIME
from sqlalchemy import ForeignKey


class TransactionModel(Base):
    __tablename__ = "transactions"

    id = Column(INTEGER, primary_key=True, unique=True, nullable=False)
    uuid = Column(VARCHAR(36), nullable=False, unique=True)
    type = Column(
        INTEGER, ForeignKey("transactions_types.id"), nullable=False, unique=False
    )
    user = Column(INTEGER, ForeignKey("users.id"), nullable=False, unique=False)
    is_success = Column(BOOLEAN, nullable=False, default=False, unique=False)
    date = Column(
        DATETIME, nullable=False, default=datetime.datetime.now(), unique=False
    )

    def __repr__(self) -> str:
        return f"{self.id} {self.uuid} {self.user} {self.date}"
