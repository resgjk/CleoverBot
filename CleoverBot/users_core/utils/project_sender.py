from users_core.utils.phrases import phrases
from users_core.utils.add_media_function import add_media
from db.models.projects import ProjectModel


class ProjectSender:
    def __init__(self, project: ProjectModel) -> None:
        self.title = project.title
        self.description = project.description
        self.photos = project.photos
        self.videos = project.videos
        self.links = project.links

    def show_project_details(self):
        text = []
        text.append(f"<b>{self.title}</b>\n\n")
        text.append(f"ℹ️ {self.description}\n\n")
        if self.links:
            for link in self.links.split(";"):
                if link:
                    text.append(f"🔗 {link}\n")
        text.append(phrases["choise_project_news"])
        text = "".join(text)
        media = add_media(text, self.photos, self.videos)

        return text, media
