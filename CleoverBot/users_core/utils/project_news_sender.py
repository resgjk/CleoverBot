from users_core.utils.add_media_function import add_media
from db.models.projects_news import ProjectNewsModel


class NewsSender:
    def __init__(self, news: ProjectNewsModel) -> None:
        self.title = news.title
        self.description = news.description
        self.photos = news.photos.split(";")[:-1]
        self.videos = news.videos.split(";")[:-1]

    def show_news_to_user(self):
        text = []
        text.append(f"<b>{self.title}</b>")
        text.append(f"{self.description}")
        text = "\n\n".join(text)
        media = add_media(text, self.photos, self.videos)

        return text, media
