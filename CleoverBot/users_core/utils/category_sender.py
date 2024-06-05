import os

from db.models.projects_categories import ProjectCategoryModel
from users_core.utils.phrases import phrases
from aiogram.types import FSInputFile


class CategorySender:
    def __init__(self, category: ProjectCategoryModel) -> None:
        self.title = category.title
        self.description = category.description
        self.media = category.media
        self.media_type = category.media_type

    def show_category_for_user(self):
        text = []
        text.append(f"<b>{self.title}</b>")
        text.append(self.description)
        text.append(phrases["choise_project"])
        text = "\n\n".join(text)

        if self.media and os.path.exists(self.media):
            media = FSInputFile(self.media)
        else:
            media = None

        return text, media
