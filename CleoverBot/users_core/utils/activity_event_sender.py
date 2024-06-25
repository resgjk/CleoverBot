import os

from aiogram.types import FSInputFile


class ActivitySender:
    def __init__(self, activity_details) -> None:
        self.title = activity_details["title"]
        self.description = activity_details["description"]

    def send_activity(self):
        text = []
        text.append(f"<b>{self.title}</b>")
        if self.description:
            text.append(f"{self.description}")
        text = "\n\n".join(text)

        return text
