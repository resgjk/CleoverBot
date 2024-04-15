from datetime import datetime, timezone

from db.base import Base

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column


class ProjectNewsModel(Base):
    __tablename__ = "projects_news"

    id: Mapped[int] = mapped_column(
        primary_key=True, unique=True, nullable=False, autoincrement=True
    )
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id"), nullable=False)
    project: Mapped["ProjectModel"] = relationship("ProjectModel", back_populates="news")  # type: ignore
    title: Mapped[str] = mapped_column(nullable=False)
    create_date: Mapped[str] = mapped_column(
        nullable=False, default=str(datetime.now(tz=timezone.utc).date())
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
        return f"{self.title} {self.project}"
