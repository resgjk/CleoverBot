from db.base import Base

from sqlalchemy.orm import relationship, mapped_column, Mapped


class ProjectCategoryModel(Base):
    __tablename__ = "projects_categories"

    id: Mapped[int] = mapped_column(
        primary_key=True, unique=True, nullable=False, autoincrement=True
    )
    title: Mapped[str] = mapped_column(unique=True, nullable=False)
    description: Mapped[str] = mapped_column(unique=False, nullable=True)
    photos: Mapped[str] = mapped_column(nullable=True)
    videos: Mapped[str] = mapped_column(nullable=True)
    projects: Mapped[list["ProjectModel"]] = relationship(
        "ProjectModel",
        back_populates="project_category",
        lazy=True,
        cascade="save-update, merge, delete",
    )

    def __repr__(self) -> str:
        return f"{self.id} {self.title}"
