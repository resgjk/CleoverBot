import datetime

from sqlalchemy import Column, Integer, VARCHAR, Boolean, DateTime
from sqlalchemy import ForeignKey
from db.database import BaseModel


class TransactionModel(BaseModel):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, unique=True, nullable=False)
    uuid = Column(VARCHAR(36), nullable=False, unique=True)
    category = Column(
        Integer, ForeignKey("categories.id"), nullable=False, unique=False
    )
    user = Column(Integer, ForeignKey("users.id"), nullable=False, unique=False)
    is_success = Column(Boolean, nullable=False, default=False, unique=False)
    date = Column(
        DateTime, nullable=False, default=datetime.datetime.now(), unique=False
    )

    def __repr__(self) -> str:
        return f"{self.id} {self.uuid} {self.category} {self.user} {self.date}"
