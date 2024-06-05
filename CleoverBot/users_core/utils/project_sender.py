import os

from db.models.projects import ProjectModel

from aiogram.types import FSInputFile


class ProjectSender:
    def __init__(self, project: ProjectModel) -> None:
        self.title = project.title
        self.description = project.description
        self.links = project.links
        self.media = project.media
        self.media_type = project.media_type

    def show_project_details(self):
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
