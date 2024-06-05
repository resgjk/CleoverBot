import os

from aiogram.types import FSInputFile


class CategorySender:
    def __init__(self, context_data) -> None:
        self.title = context_data.get("title")
        self.description = context_data.get("description")

        self.photos = context_data.get("photos")
        self.media = context_data.get("media")
        self.media_type = context_data.get("media_type")

    def show_category_detail_for_admin(self):
        text = []
        text.append(f"<b>Название</b>: {self.title}")
        text.append(f"<b>Описание</b>: {self.description}")
        text = "\n\n".join(text)
        if self.media and os.path.exists(self.media):
            media = FSInputFile(self.media)
        else:
            media = None

        return text, media
