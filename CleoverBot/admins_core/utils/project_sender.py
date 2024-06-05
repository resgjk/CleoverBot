import os

from aiogram.types import FSInputFile


class ProjectSender:
    def __init__(self, context_data=None, project_data=None) -> None:
        if context_data:
            self.title = context_data.get("title")
            self.category = context_data.get("category_title")
            self.description = context_data.get("description")
            self.links = context_data.get("links")
            self.media = context_data.get("media")
            self.media_type = context_data.get("media_type")
        elif project_data:
            self.title = project_data["title"]
            self.description = project_data["description"]
            self.links = project_data["links"]
            self.media = project_data["media"]
            self.media_type = project_data["media_type"]

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

        if self.media and os.path.exists(self.media):
            media = FSInputFile(self.media)
        else:
            media = None

        return text, media

    def send_project(self):
        text = []
        text.append(f"<b>{self.title}\n\n</b>")
        text.append(f"{self.description}\n\n")
        if self.links:
            text.append("🔗 <b>Links:</b>\n")
            links_lst = []
            for link in self.links.split(";")[:-1]:
                if link:
                    links_lst.append(f"• {link}\n")
            if links_lst:
                text.append("".join(links_lst) + "\n")
        text = "".join(text)

        if self.media and os.path.exists(self.media):
            media = FSInputFile(self.media)
        else:
            media = None

        return text, media
