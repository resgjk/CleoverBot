import datetime

from sqlalchemy import Column, Integer, Boolean, Date
from db.database import BaseModel


class UserModel(BaseModel):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, unique=True, nullable=False)
    user_id = Column(Integer, unique=True, nullable=False)
    is_subscriber = Column(Boolean, nullable=False, default=False, unique=False)
    subscriber_until = Column(Date, nullable=True, unique=False)

    def __repr__(self) -> str:
        return f"{self.id} {self.user_id} {self.is_subscriber} {self.subscriber_until}"
