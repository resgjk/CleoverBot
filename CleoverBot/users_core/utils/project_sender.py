from users_core.utils.phrases import phrases
from users_core.utils.add_media_function import add_media
from db.models.projects import ProjectModel


class ProjectSender:
    def __init__(self, project: ProjectModel) -> None:
        self.title = project.title
        self.description = project.description
        self.photos = project.photos
        if self.photos:
            self.photos = project.photos.split(";")[:-1]
        self.videos = project.videos
        if self.videos:
            self.videos = project.videos.split(";")[:-1]
        self.links = project.links

    def show_project_details(self):
        text = []
        text.append(f"<b>{self.title}</b>")
        text.append(f"{self.description}")
        if self.links:
            links_lst = []
            for link in self.links.split(";")[:-1]:
                if link:
                    links_lst.append(f"🔗 {link}\n")
            if links_lst:
                text.append("".join(links_lst))
        text = "\n\n".join(text)
        media = add_media(text, self.photos, self.videos)

        return text, media
