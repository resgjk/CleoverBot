from db.base import Base

from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, mapped_column, Mapped


class ProjectModel(Base):
    __tablename__ = "projects"

    id: Mapped[int] = mapped_column(
        primary_key=True, unique=True, nullable=False, autoincrement=True
    )
    title: Mapped[str] = mapped_column(nullable=False)
    category_id: Mapped[int] = mapped_column(
        ForeignKey("projects_categories.id"), nullable=False
    )
    category: Mapped["ProjectCategoryModel"] = relationship("projects_categories", back_populates="projects")  # type: ignore
    description: Mapped[str] = mapped_column(unique=False, nullable=True)
    photos: Mapped[str] = mapped_column(nullable=True)
    videos: Mapped[str] = mapped_column(nullable=True)
    links: Mapped[str] = mapped_column(nullable=True)
    news: Mapped[list["ProjectNewsModel"]] = relationship(
        "ProjectNewsModel", back_populates="project", lazy=True
    )

    def __repr__(self) -> str:
        return f"{self.id}"
