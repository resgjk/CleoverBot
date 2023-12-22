from datetime import date, time, datetime

from db.base import Base

from sqlalchemy import DATE, BIGINT, TIME
from sqlalchemy.orm import Mapped, mapped_column


class PostModel(Base):
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(primary_key=True, unique=True, nullable=False)
    owner_id: Mapped[int] = mapped_column(BIGINT, nullable=False, unique=False)
    title: Mapped[str] = mapped_column(nullable=False)
    category: Mapped[str] = mapped_column(nullable=False, unique=False)
    bank: Mapped[str] = mapped_column(nullable=True)
    create_date: Mapped[str] = mapped_column(
        nullable=False, default=str(datetime.now().date())
    )
    start_date: Mapped[str] = mapped_column(nullable=True)
    start_time: Mapped[str] = mapped_column(nullable=True)
    end_date: Mapped[str] = mapped_column(nullable=True)
    end_time: Mapped[str] = mapped_column(nullable=True)
    short_description: Mapped[str] = mapped_column(nullable=False)
    full_description: Mapped[str] = mapped_column(nullable=False)
    photos: Mapped[str] = mapped_column(nullable=True)
    videos: Mapped[str] = mapped_column(nullable=True)

    def __repr__(self) -> str:
        return f"{self.title} {self.owner_id}"
