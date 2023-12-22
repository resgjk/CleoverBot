from db.base import Base

from sqlalchemy import BIGINT
from sqlalchemy.orm import mapped_column, Mapped


class AdminModel(Base):
    __tablename__ = "admins"

    id: Mapped[int] = mapped_column(primary_key=True, unique=True, nullable=False)
    user_id: Mapped[int] = mapped_column(BIGINT, unique=True, nullable=False)
    is_super_admin: Mapped[bool] = mapped_column(
        nullable=False, default=False, unique=False
    )

    def __repr__(self) -> str:
        return f"{self.id} {self.user_id} {self.is_super_admin}"
