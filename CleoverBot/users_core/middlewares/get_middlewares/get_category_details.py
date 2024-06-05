from typing import Callable, Dict, Any, Awaitable

from db.models.projects_categories import ProjectCategoryModel

from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery

from sqlalchemy.orm import sessionmaker
from sqlalchemy import select
from sqlalchemy.engine import ScalarResult


class CategoryDetailsMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[CallbackQuery, Dict[str, Any]], Awaitable[Any]],
        event: CallbackQuery,
        data: Dict[str, Any],
    ) -> Any:
        session_maker: sessionmaker = data["session_maker"]
        async with session_maker() as session:
            async with session.begin():
                res: ScalarResult = await session.execute(
                    select(ProjectCategoryModel).where(
                        ProjectCategoryModel.id == int(event.data.split("_")[-1])
                    )
                )
                category = res.scalars().one_or_none()
                data["category"] = category
                return await handler(event, data)
