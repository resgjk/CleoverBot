from db.base import Base

from sqlalchemy import ForeignKey, BIGINT
from sqlalchemy.orm import Mapped, mapped_column


class UserToProjectModel(Base):
    __tablename__ = "users_to_projects"

    user_id: Mapped[int] = mapped_column(
        BIGINT, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True
    )
    project_id: Mapped[int] = mapped_column(
        ForeignKey("projects.id", ondelete="CASCADE"), primary_key=True
    )

    def __repr__(self) -> str:
        return f"{self.user_id} - {self.activity_id}"
