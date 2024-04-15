from db.base import Base

from sqlalchemy.orm import relationship, mapped_column, Mapped


class ActivityModel(Base):
    __tablename__ = "activities"

    id: Mapped[int] = mapped_column(
        primary_key=True, unique=True, nullable=False, autoincrement=True
    )
    title: Mapped[str] = mapped_column(unique=True, nullable=False)
    users: Mapped[list["UserModel"]] = relationship(  # type: ignore
        back_populates="activities", secondary="users_to_activities"
    )

    def __repr__(self) -> str:
        return f"{self.id} {self.title}"
