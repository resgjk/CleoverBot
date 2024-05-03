from users_core.utils.add_media_function import add_media
from db.models.projects_news import ProjectNewsModel


class NewsSender:
    def __init__(self, news: ProjectNewsModel) -> None:
        self.title = news.title
        self.description = news.description
        self.photos = news.photos
        self.videos = news.videos

    def show_news_to_user(self):
        text = []
        text.append(f"🚨 <b>{self.title}</b>\n\n")
        text.append(f"ℹ️ {self.description}\n\n")
        text = "".join(text)
        media = add_media(text, self.photos, self.videos)

        return text, media
