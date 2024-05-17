from users_core.utils.add_media_function import add_media


class CalendarEventSender:
    def __init__(self, event_datails) -> None:
        self.title = event_datails["title"]
        self.full_description = event_datails["full_description"]
        self.photos = event_datails["photos"]
        if self.photos:
            self.photos = event_datails["photos"].split(";")[:-1]
        self.videos = event_datails["videos"]
        if self.videos:
            self.videos = event_datails["videos"].split(";")[:-1]

    def send_event(self):
        text = []
        text.append(f"<b>{self.title}</b>")
        text.append(f"{self.full_description}")
        text = "\n\n".join(text)
        media = add_media(photos=self.photos, videos=self.videos)

        return text, media
