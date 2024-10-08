from apsched.send_notification import send_notifications

import os
from datetime import datetime, timedelta, timezone, date, time

from aiogram.types import FSInputFile


class PostSender:
    def __init__(self, context_data) -> None:
        self.title = context_data.get("title")
        self.category = context_data.get("category")
        self.bank = context_data.get("bank")
        self.start_date = context_data.get("start_date")
        self.start_time = context_data.get("start_time")
        self.end_date = context_data.get("end_date")
        self.end_time = context_data.get("end_time")
        self.short_description = context_data.get("short_description")
        self.full_description = context_data.get("full_description")
        self.media = context_data.get("media")
        self.media_type = context_data.get("media_type")

    def show_post_detail_for_admin(self):
        text = []
        text.append(f"<b>Название</b>: {self.title}")
        text.append(f"<b>Категория</b>: {self.category}")
        text.append(f"<b>Бюджет</b>: {self.bank}")
        if self.start_date:
            text.append(
                f"<b>Дата начала</b>: {'.'.join(str(self.start_date).split('-')[::-1])}"
            )
        if self.start_time:
            text.append(
                f"<b>Время начала</b>: {':'.join(str(self.start_time).split(':')[:2])}"
            )
        if self.end_date:
            text.append(
                f"<b>Дата окончания</b>: {'.'.join(str(self.end_date).split('-')[::-1])}"
            )
        if self.end_time:
            text.append(
                f"<b>Время окончания</b>: {':'.join(str(self.end_time).split(':')[:2])}"
            )
        text.append(f"<b>Краткое описание</b>: {self.short_description}")
        text.append(f"<b>Подробное описание</b>: {self.full_description}")
        text = "\n\n".join(text)

        if self.media and os.path.exists(self.media):
            media = FSInputFile(self.media)
        else:
            media = None

        return text, media

    def notification_sender(self, datetime_start_date_time, scheduler):
        post_details = {
            "title": self.title,
            "category": self.category,
            "bank": self.bank,
            "start_date": self.start_date,
            "start_time": self.start_time,
            "end_date": self.end_date,
            "end_time": self.end_time,
            "full_description": self.full_description,
            "media": self.media,
            "media_type": self.media_type,
        }

        times = [
            [1, "1 Hour"],
            [3, "3 Hours"],
            [6, "6 Hours"],
            [12, "12 Hours"],
        ]
        for time in times:
            scheduler.add_job(
                send_notifications,
                trigger="date",
                run_date=datetime_start_date_time - timedelta(hours=time[0]),
                kwargs={
                    "post_details": post_details,
                    "notification": time[1],
                },
            )

    def send_post_to_users(self, scheduler):
        if self.start_date and self.start_time:
            datetime_start_date_time = datetime.combine(
                date.fromisoformat(self.start_date),
                time.fromisoformat(self.start_time),
                tzinfo=timezone.utc,
            )
            self.notification_sender(
                datetime_start_date_time=datetime_start_date_time,
                scheduler=scheduler,
            )

        text = []
        text.append(f"<b>{self.title}</b>")
        text.append(f"{self.full_description}")
        text = "\n\n".join(text)

        if self.media and os.path.exists(self.media):
            media = FSInputFile(self.media)
        else:
            media = None

        return text, media
