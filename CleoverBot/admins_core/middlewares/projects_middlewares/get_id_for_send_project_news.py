from db.models.projects import ProjectModel
from db.models.projects_news import ProjectNewsModel

from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from sqlalchemy.orm import sessionmaker, selectinload
from sqlalchemy import select
from sqlalchemy.engine import ScalarResult


class SendNewsMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[CallbackQuery, Dict[str, Any]], Awaitable[Any]],
        event: CallbackQuery,
        data: Dict[str, Any],
    ) -> Any:
        session_maker: sessionmaker = data["session_maker"]
        state: FSMContext = data["state"]
        context_data = await state.get_data()
        owner_id = context_data.get("owner_id")
        project_news_id = context_data.get("project_news_id")
        title = context_data.get("title")
        description = context_data.get("description")
        photos = context_data.get("photos")
        videos = context_data.get("videos")
        users_id = []
        async with session_maker() as session:
            async with session.begin():
                if title:
                    new_news = ProjectNewsModel(
                        project_id=project_news_id, title=title, description=description
                    )
                    if photos:
                        new_news.photos = photos
                    if videos:
                        new_news.videos = videos
                    session.add(new_news)

                project_res: ScalarResult = await session.execute(
                    select(ProjectModel)
                    .options(selectinload(ProjectModel.users))
                    .where(ProjectModel.id == project_news_id)
                )
                current_project: ProjectModel = project_res.scalars().one_or_none()
                if current_project:
                    for user in current_project.users:
                        if user.user_id != owner_id and user.is_subscriber:
                            users_id.append(user.user_id)
                data["users_id"] = users_id
                await session.commit()
        return await handler(event, data)
