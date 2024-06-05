import os

from aiogram.types import FSInputFile


class CalendarEventSender:
    def __init__(self, event_datails) -> None:
        self.title = event_datails["title"]
        self.full_description = event_datails["full_description"]
        self.media = event_datails["media"]
        self.media_type = event_datails["media_type"]

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
