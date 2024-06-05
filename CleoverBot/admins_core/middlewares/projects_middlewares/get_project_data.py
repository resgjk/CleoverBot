from typing import Callable, Dict, Any, Awaitable

from db.models.projects import ProjectModel

from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery

from sqlalchemy.orm import sessionmaker
from sqlalchemy import select
from sqlalchemy.engine import ScalarResult


class ProjectDetailsMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[CallbackQuery, Dict[str, Any]], Awaitable[Any]],
        event: CallbackQuery,
        data: Dict[str, Any],
    ) -> Any:
        session_maker: sessionmaker = data["session_maker"]
        project_id = int(event.data.split("_")[-1])
        async with session_maker() as session:
            async with session.begin():
                res: ScalarResult = await session.execute(
                    select(ProjectModel).where(ProjectModel.id == project_id)
                )
                project: ProjectModel = res.scalars().one_or_none()
                if project:
                    project_data = {
                        "id": project.id,
                        "title": project.title,
                        "description": project.description,
                        "links": project.links,
                        "media": project.media,
                        "media_type": project.media_type,
                    }
                    data["project_data"] = project_data
                    data["result"] = "success"
                else:
                    data["project_data"] = {}
                    data["result"] = "error"
        return await handler(event, data)
