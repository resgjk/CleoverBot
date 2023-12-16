from sqlalchemy import Column, BOOLEAN, INTEGER, BIGINT, ForeignKey
from db.base import Base


class AdminModel(Base):
    __tablename__ = "admins"

    id = Column(INTEGER, primary_key=True, unique=True, nullable=False)
    user_id = Column(BIGINT, ForeignKey("users.id"), unique=True, nullable=False)
    is_super_admin = Column(BOOLEAN, nullable=False, default=False, unique=False)

    def __repr__(self) -> str:
        return f"{self.id} {self.user_id} {self.is_super_admin}"
