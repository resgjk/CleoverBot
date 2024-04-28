from apsched.send_notification import send_notifications

from aiogram.types import InputMediaPhoto, InputMediaVideo, FSInputFile
from datetime import datetime, timedelta, timezone


class ProjectSender:
    def __init__(self, context_data=None, project_data=None) -> None:
        if context_data:
            self.title = context_data.get("title")
            self.category = context_data.get("category_title")
            self.description = context_data.get("description")
            self.links = context_data.get("links")
            self.photos = context_data.get("photos").split(";")[:-1]
            self.videos = context_data.get("videos").split(";")[:-1]
        elif project_data:
            self.title = project_data["title"]
            self.description = project_data["description"]
            self.links = project_data["links"]
            self.photos = project_data["photos"].split(";")[:-1]
            self.videos = project_data["videos"].split(";")[:-1]

    def add_media(self, text):
        media = []
        if self.photos:
            for photo in self.photos:
                if not media:
                    media.append(
                        InputMediaPhoto(
                            type="photo", media=FSInputFile(path=photo), caption=text
                        )
                    )
                else:
                    media.append(
                        InputMediaPhoto(type="photo", media=FSInputFile(path=photo))
                    )
        if self.videos:
            for video in self.videos:
                if not media:
                    media.append(
                        InputMediaVideo(
                            type="video", media=FSInputFile(path=video), caption=text
                        )
                    )
                else:
                    media.append(
                        InputMediaVideo(type="video", media=FSInputFile(path=video))
                    )
        return media

    def show_project_detail_for_admin(self):
        text = []
        text.append(f"<b>Название</b>: {self.title}")
        text.append(f"<b>Категория</b>: {self.category}")
        text.append(f"<b>Описание</b>: {self.description}")
        if self.links:
            links_str = f"<b>Ссылки</b>:\n"
            for link in self.links.split(";"):
                links_str += link + "\n"
            text.append(links_str)
        text = "\n\n".join(text)
        media = self.add_media(text)

        return text, media

    def send_project_to_users(self):
        text = []
        text.append(f"🆕 <b>{self.title}</b>\n\n")
        text.append(f"ℹ️ {self.description}\n\n")
        if self.links:
            for link in self.links.split(";"):
                if link:
                    text.append(f"🔗 {link}\n")
        text = "".join(text)
        media = self.add_media(text)

        return text, media

    def show_for_add_news_or_delete(self):
        text = []
        text.append(f"<b>{self.title}</b>\n\n")
        text.append(f"ℹ️ {self.description}\n\n")
        if self.links:
            for link in self.links.split(";"):
                if link:
                    text.append(f"🔗 {link}\n")
        text = "".join(text)
        media = self.add_media(text)

        return text, media
