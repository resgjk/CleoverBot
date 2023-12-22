from datetime import date

from db.base import Base

from sqlalchemy import BIGINT, DATE
from sqlalchemy.orm import relationship, mapped_column, Mapped


class UserModel(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, unique=True, nullable=False)
    user_id: Mapped[int] = mapped_column(BIGINT, unique=True, nullable=False)
    is_subscriber: Mapped[bool] = mapped_column(
        nullable=False, default=False, unique=False
    )
    subscriber_until: Mapped[str] = mapped_column(nullable=True, unique=False)
    bank: Mapped[str] = mapped_column(nullable=False, default="Zero bank")
    notification: Mapped[str] = mapped_column(nullable=False, default="1 Hour")
    activities: Mapped[list["ActivityModel"]] = relationship(
        back_populates="users", secondary="users_to_activities"
    )

    def __repr__(self) -> str:
        return f"{self.id} {self.user_id} {self.is_subscriber} {self.subscriber_until} {self.bank} {self.notification}"
