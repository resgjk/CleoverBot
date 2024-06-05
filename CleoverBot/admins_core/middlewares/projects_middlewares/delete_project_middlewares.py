from typing import Callable, Dict, Any, Awaitable

from db.models.projects import ProjectModel

from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery

from sqlalchemy.orm import sessionmaker
from sqlalchemy import select
from sqlalchemy.engine import ScalarResult


class DeleteProjectMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[CallbackQuery, Dict[str, Any]], Awaitable[Any]],
        event: CallbackQuery,
        data: Dict[str, Any],
    ) -> Any:
        session_maker: sessionmaker = data["session_maker"]
        project_id = int(event.data.split("_")[-1])
        try:
            async with session_maker() as session:
                async with session.begin():
                    res: ScalarResult = await session.execute(
                        select(ProjectModel).where(ProjectModel.id == project_id)
                    )
                    current_project: ProjectModel = res.scalars().one_or_none()
                    if current_project:
                        await session.delete(current_project)
                        await session.commit()
                        data["result"] = "success"
                    else:
                        data["result"] = "was_deleted"
        except Exception:
            data["result"] = "error"
        return await handler(event, data)
