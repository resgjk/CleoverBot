import os

from db.models.projects_news import ProjectNewsModel

from aiogram.types import FSInputFile


class NewsSender:
    def __init__(self, news: ProjectNewsModel) -> None:
        self.title = news.title
        self.description = news.description
        self.media = news.media
        self.media_type = news.media_type

    def show_news_to_user(self):
        text = []
        text.append(f"<b>{self.title}</b>")
        text.append(f"{self.description}")
        text = "\n\n".join(text)

        if self.media and os.path.exists(self.media):
            media = FSInputFile(self.media)
        else:
            media = None

        return text, media
