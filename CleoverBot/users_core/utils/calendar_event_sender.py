import os

from aiogram.types import FSInputFile


class CalendarEventSender:
    def __init__(self, event_details) -> None:
        self.title = event_details["title"]
        self.full_description = event_details["full_description"]
        self.media = event_details["media"]
        self.media_type = event_details["media_type"]

    def send_event(self):
        text = []
        text.append(f"<b>{self.title}</b>")
        text.append(f"{self.full_description}")
        text = "\n\n".join(text)

        if self.media and os.path.exists(self.media):
            media = FSInputFile(self.media)
        else:
            media = None

        return text, media
