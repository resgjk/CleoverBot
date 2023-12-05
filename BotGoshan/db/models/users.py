import datetime

from sqlalchemy.orm import Mapped, mapped_column
from db.database import Base


class UserModel(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        primary_key=True, nullable=False, autoincrement=True
    )
    user_id: Mapped[int] = mapped_column(unique=True, nullable=False)
    is_subscriber: Mapped[bool] = mapped_column(nullable=False, default=False)
    subscriber_until: Mapped[datetime.date] = mapped_column(nullable=True)

    def __repr__(self) -> str:
        return f"{self.id} {self.user_id} {self.is_subscriber} {self.subscriber_until}"
