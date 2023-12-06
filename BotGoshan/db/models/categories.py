from sqlalchemy import Column, Integer, Text
from db.database import BaseModel


class CategoryModel(BaseModel):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, unique=True, nullable=False)
    title = Column(Text, nullable=False, unique=True)

    def __repr__(self) -> str:
        return f"{self.id} {self.title}"
