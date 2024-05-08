from users_core.utils.phrases import phrases
from users_core.utils.add_media_function import add_media
from db.models.projects import ProjectModel


class ProjectSender:
    def __init__(self, project: ProjectModel) -> None:
        self.title = project.title
        self.description = project.description
        self.photos = project.photos.split(";")[:-1]
        self.videos = project.videos.split(";")[:-1]
        self.links = project.links

    def show_project_details(self):
        text = []
        text.append(f"<b>{self.title}</b>")
        text.append(f"{self.description}")
        if self.links:
            links_lst = []
            for link in self.links.split(";"):
                if link:
                    links_lst.append(f"🔗 {link}\n")
            text.append("".join(links_lst))
        text.append(phrases["choise_project_news"])
        text = "\n\n".join(text)
        media = add_media(text, self.photos, self.videos)

        return text, media
