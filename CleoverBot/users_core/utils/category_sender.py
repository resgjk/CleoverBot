from users_core.utils.add_media_function import add_media
from db.models.projects_categories import ProjectCategoryModel


class CategorySender:
    def __init__(self, category: ProjectCategoryModel) -> None:
        self.title = category.title
        self.description = category.description
        self.photos = category.photos
        self.videos = category.videos

    def show_category_for_user(self):
        text = []
        text.append(f"<b>{self.title}</b>")
        text.append(self.description)
        text = "\n\n".join(text)
        media = add_media(text, self.photos, self.videos)

        return text, media
