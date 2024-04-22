from db.models.projects_categories import ProjectCategoryModel

from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import Message, ContentType

from sqlalchemy.orm import sessionmaker
from sqlalchemy import select
from sqlalchemy.engine import ScalarResult


class DeleteProjectsCategoryMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any],
    ) -> Any:
        session_maker: sessionmaker = data["session_maker"]
        if event.content_type == ContentType.TEXT:
            async with session_maker() as session:
                async with session.begin():
                    res: ScalarResult = await session.execute(
                        select(ProjectCategoryModel).where(
                            ProjectCategoryModel.title == event.text
                        )
                    )
                    current_category: ProjectCategoryModel = res.scalars().one_or_none()
                    if current_category:
                        await session.delete(current_category)
                        await session.commit()
                        data["result"] = "success"
                    else:
                        data["result"] = "not_in_db"
        else:
            data["result"] = "invalid"
        return await handler(event, data)
