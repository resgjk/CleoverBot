from sqlalchemy import Column, DATE, INTEGER, BIGINT, TEXT, VARCHAR, TIME
from db.base import Base


class PostModel(Base):
    __tablename__ = "posts"

    id = Column(INTEGER, primary_key=True, unique=True, nullable=False)
    owner_id = Column(BIGINT, nullable=False, unique=False)
    title = Column(TEXT, nullable=False)
    category = Column(VARCHAR(25), nullable=True, unique=False)
    bank = Column(VARCHAR(20), nullable=True)
    create_date = Column(DATE, nullable=False)
    start_date = Column(DATE, nullable=True)
    start_time = Column(TIME, nullable=True)
    end_date = Column(DATE, nullable=True)
    end_time = Column(TIME, nullable=True)
    short_description = Column(TEXT, nullable=False)
    full_description = Column(TEXT, nullable=False)
    photos = Column(TEXT, nullable=True)
    videos = Column(TEXT, nullable=True)

    def __repr__(self) -> str:
        return f"{self.title} {self.owner_id}"
