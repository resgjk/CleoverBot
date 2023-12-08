from sqlalchemy import Column, BOOLEAN, DATE, INTEGER, BIGINT
from db.base import Base


class UserModel(Base):
    __tablename__ = "users"

    id = Column(INTEGER, primary_key=True, unique=True, nullable=False)
    user_id = Column(BIGINT, unique=True, nullable=False)
    is_subscriber = Column(BOOLEAN, nullable=False, default=False, unique=False)
    subscriber_until = Column(DATE, nullable=True, unique=False)

    def __repr__(self) -> str:
        return f"{self.id} {self.user_id} {self.is_subscriber} {self.subscriber_until}"
