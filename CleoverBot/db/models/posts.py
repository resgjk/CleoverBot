from datetime import datetime, timezone, date, time
from typing import Literal

from db.base import Base

from sqlalchemy import BIGINT, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship


class PostModel(Base):
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(
        primary_key=True, unique=True, nullable=False, autoincrement=True
    )
    owner_id: Mapped[int] = mapped_column(BIGINT, nullable=False, unique=False)
    title: Mapped[str] = mapped_column(nullable=False)
    category_id: Mapped[int] = mapped_column(
        ForeignKey("activities.id"), nullable=False
    )
    category: Mapped["ActivityModel"] = relationship("ActivityModel", back_populates="posts")  # type: ignore
    bank: Mapped[
        Literal["Zero bank", "$100 - 1000", "$1000 - 10000", "$10k+", "Любой бюджет"]
    ]
    create_date: Mapped[date] = mapped_column(
        nullable=False, default=datetime.now(tz=timezone.utc).date()
    )
    start_date: Mapped[date] = mapped_column(nullable=True)
    start_time: Mapped[time] = mapped_column(nullable=True)
    end_date: Mapped[date] = mapped_column(nullable=True)
    end_time: Mapped[time] = mapped_column(nullable=True)
    short_description: Mapped[str] = mapped_column(nullable=False)
    full_description: Mapped[str] = mapped_column(nullable=False)
    media: Mapped[str] = mapped_column(nullable=True)
    media_type: Mapped[Literal["photo", "video"]] = mapped_column(nullable=True)

    def __repr__(self) -> str:
        return f"{self.title} {self.owner_id}"
