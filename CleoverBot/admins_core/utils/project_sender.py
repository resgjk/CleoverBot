from admins_core.utils.add_media_function import add_media


class ProjectSender:
    def __init__(self, context_data=None, project_data=None) -> None:
        if context_data:
            self.title = context_data.get("title")
            self.category = context_data.get("category_title")
            self.description = context_data.get("description")
            self.links = context_data.get("links")
            self.photos = context_data.get("photos").split(";")[:-1]
            self.videos = context_data.get("videos").split(";")[:-1]
        elif project_data:
            self.title = project_data["title"]
            self.description = project_data["description"]
            self.links = project_data["links"]
            self.photos = project_data["photos"].split(";")[:-1]
            self.videos = project_data["videos"].split(";")[:-1]

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
        media = add_media(text, self.photos, self.videos)

        return text, media

    def send_project(self):
        text = []
        text.append(f"<b>{self.title}</b>")
        text.append(f"{self.description}")
        if self.links:
            links_lst = []
            for link in self.links.split(";"):
                if link:
                    links_lst.append(f"🔗 {link}\n")
            text.append("".join(links_lst))
        text = "\n\n".join(text)
        media = add_media(text, self.photos, self.videos)

        return text, media
