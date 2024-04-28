from db.models.projects_categories import ProjectCategoryModel
from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery

from sqlalchemy.orm import sessionmaker
from sqlalchemy import select
from sqlalchemy.engine import ScalarResult


class ChoiseCategoryMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[CallbackQuery, Dict[str, Any]], Awaitable[Any]],
        event: CallbackQuery,
        data: Dict[str, Any],
    ) -> Any:
        session_maker: sessionmaker = data["session_maker"]
        category_id = int(event.data.split("_")[-1])
        async with session_maker() as session:
            async with session.begin():
                res: ScalarResult = await session.execute(
                    select(ProjectCategoryModel).where(
                        ProjectCategoryModel.id == category_id
                    )
                )
                current_category: ProjectCategoryModel = res.scalars().one_or_none()
                if current_category:
                    choisen_category = {
                        "id": current_category.id,
                        "title": current_category.title,
                    }
                    data["choisen_category"] = choisen_category
                else:
                    data["error"] = True
                    data["choisen_category"] = None
        return await handler(event, data)
