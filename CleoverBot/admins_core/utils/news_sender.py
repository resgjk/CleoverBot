from admins_core.utils.add_media_function import add_media


class NewsSender:
    def __init__(self, context_data) -> None:
        self.title = context_data.get("title")
        self.description = context_data.get("description")
        self.photos = context_data.get("photos")
        if self.photos:
            self.photos = context_data.get("photos").split(";")[:-1]
        self.videos = context_data.get("videos")
        if self.videos:
            self.videos = context_data.get("videos").split(";")[:-1]

    def show_news_detail_for_admin(self):
        text = []
        text.append(f"<b>Название</b>: {self.title}")
        text.append(f"<b>Описание</b>: {self.description}")
        text = "\n\n".join(text)
        media = add_media(text, self.photos, self.videos)

        return text, media

    def send_news_to_users(self):
        text = []
        text.append(f"<b>{self.title}</b>")
        text.append(f"{self.description}")
        text = "\n\n".join(text)
        media = add_media(text, self.photos, self.videos)

        return text, media
