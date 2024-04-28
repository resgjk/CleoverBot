from aiogram.types import InputMediaPhoto, InputMediaVideo, FSInputFile


class CalendarEventSender:
    def __init__(self, event_datails) -> None:
        self.title = event_datails["title"]
        self.start_date = event_datails["start_date"]
        self.start_time = event_datails["start_time"]
        self.end_date = event_datails["end_date"]
        self.end_time = event_datails["end_time"]
        self.full_description = event_datails["full_description"]
        self.photos = event_datails["photos"]
        if self.photos:
            self.photos = event_datails["photos"].split(";")[:-1]
        self.videos = event_datails["videos"]
        if self.videos:
            self.videos = event_datails["videos"].split(";")[:-1]

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

    def send_event(self):
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
