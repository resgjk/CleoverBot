from datetime import datetime
from typing import Literal

from db.base import Base

from sqlalchemy import ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship


class ProjectNewsModel(Base):
    __tablename__ = "projects_news"

    id: Mapped[int] = mapped_column(
        primary_key=True, unique=True, nullable=False, autoincrement=True
    )
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id"), nullable=False)
    project: Mapped["ProjectModel"] = relationship("ProjectModel", back_populates="news")  # type: ignore
    title: Mapped[str] = mapped_column(nullable=False)
    create_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
    description: Mapped[str] = mapped_column(nullable=False)
    media: Mapped[str] = mapped_column(nullable=True)
    media_type: Mapped[Literal["photo", "video"]] = mapped_column(nullable=True)

    def __repr__(self) -> str:
        return f"{self.title} {self.project}"
