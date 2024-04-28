from apsched.send_notification import send_notifications

from aiogram.types import InputMediaPhoto, InputMediaVideo, FSInputFile
from datetime import datetime, timedelta, timezone


class PostSender:
    def __init__(self, bot, context_data) -> None:
        self.bot = bot

        self.title = context_data.get("title")
        self.category = context_data.get("category")
        self.bank = context_data.get("bank")
        self.start_date = context_data.get("start_date")
        self.start_time = context_data.get("start_time")
        self.end_date = context_data.get("end_date")
        self.end_time = context_data.get("end_time")
        self.short_description = context_data.get("short_description")
        self.full_description = context_data.get("full_description")
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

    def show_post_detail_for_admin(self):
        text = []
        text.append(f"<b>Название</b>: {self.title}")
        text.append(f"<b>Категория</b>: {self.category}")
        text.append(f"<b>Бюджет</b>: {self.bank}")
        if self.start_date:
            text.append(
                f"<b>Дата начала</b>: {'.'.join(self.start_date.split('-')[::-1])}"
            )
        if self.start_time:
            text.append(f"<b>Время начала</b>: {self.start_time}")
        if self.end_date:
            text.append(
                f"<b>Дата окончания</b>: {'.'.join(self.end_date.split('-')[::-1])}"
            )
        if self.end_time:
            text.append(f"<b>Время окончания</b>: {self.end_time}")
        text.append(f"<b>Краткое описание</b>: {self.short_description}")
        text.append(f"<b>Подробное описание</b>: {self.full_description}")
        text = "\n\n".join(text)
        media = self.add_media(text)

        return text, media

    def notification_sender(self, datetime_start_date_time, session_maker, scheduler):
        post_details = {
            "title": self.title,
            "category": self.category,
            "bank": self.bank,
            "start_date": self.start_date,
            "start_time": self.start_time,
            "end_date": self.end_date,
            "end_time": self.end_time,
            "full_description": self.full_description,
            "photos": self.photos,
            "videos": self.videos,
            "title": self.title,
        }

        times = [
            [1, "Hour"],
            [3, "Hours"],
            [6, "Hours"],
            [12, "Hours"],
        ]
        for time in times:
            scheduler.add_job(
                send_notifications,
                trigger="date",
                run_date=datetime_start_date_time - timedelta(hours=time[0]),
                kwargs={
                    "bot": self.bot,
                    "session_maker": session_maker,
                    "post_details": post_details,
                    "notification": time[1],
                },
            )

    def send_post_to_users(self, session_maker, scheduler):
        if self.start_date and self.start_time:
            valid_date = list(map(int, self.start_date.split("-")[::-1]))
            valid_time = list(map(int, self.start_time.split(":")))
            datetime_start_date_time = datetime(
                day=valid_date[0],
                month=valid_date[1],
                year=valid_date[2],
                hour=valid_time[0],
                minute=valid_time[1],
                tzinfo=timezone.utc,
            )
            self.notification_sender(
                datetime_start_date_time=datetime_start_date_time,
                session_maker=session_maker,
                scheduler=scheduler,
            )

        text = []
        text.append(f"📢 <b>{self.title}</b>\n\n")
        text.append(f"ℹ️ {self.full_description}\n\n")
        if self.start_date:
            date = ".".join(self.start_date.split("-")[::-1])
            if self.start_time:
                text.append(f"🗓️ Start date: {date}, {self.start_time}\n")
            else:
                text.append(f"🗓️ Start date: {date}\n")
        if self.end_date:
            date = ".".join(self.end_date.split("-")[::-1])
            if self.end_time:
                text.append(f"🏁 End date: {date}, {self.end_time}")
            else:
                text.append(f"🏁 End date: {date}")
        text = "".join(text)
        media = self.add_media(text)

        return text, media
