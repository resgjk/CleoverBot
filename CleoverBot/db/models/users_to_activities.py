from db.base import Base

from sqlalchemy import ForeignKey, BIGINT
from sqlalchemy.orm import Mapped, mapped_column


class UserToActivityModel(Base):
    __tablename__ = "users_to_activities"

    user_id: Mapped[int] = mapped_column(
        BIGINT, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True
    )
    activity_id: Mapped[int] = mapped_column(
        ForeignKey("activities.id", ondelete="CASCADE"), primary_key=True
    )

    def __repr__(self) -> str:
        return f"{self.user_id} - {self.activity_id}"
