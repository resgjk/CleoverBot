from db.base import Base

from sqlalchemy import Column, INTEGER, TEXT


class TransactionTypeModel(Base):
    __tablename__ = "transactions_types"

    id = Column(INTEGER, primary_key=True, unique=True, nullable=False)
    title = Column(TEXT, nullable=False, unique=True)

    def __repr__(self) -> str:
        return f"{self.id} {self.title}"
