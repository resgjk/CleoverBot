from apsched.send_notification import send_notifications

from aiogram.types import InputMediaPhoto, InputMediaVideo, FSInputFile
from datetime import datetime, timedelta, timezone


class CategorySender:
    def __init__(self, context_data) -> None:
        self.title = context_data.get("title")
        self.description = context_data.get("description")
        self.photos = context_data.get("photos").split(";")[:-1]
        self.videos = context_data.get("videos").split(";")[:-1]

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

    def show_category_detail_for_admin(self):
        text = []
        text.append(f"<b>Название</b>: {self.title}")
        text.append(f"<b>Описание</b>: {self.description}")
        text = "\n\n".join(text)
        media = self.add_media(text)

        return text, media
