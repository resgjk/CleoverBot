from typing import Callable, Dict, Any, Awaitable

from db.models.projects_categories import ProjectCategoryModel

from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from sqlalchemy.orm import sessionmaker


class SaveProjectsCategoryMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[CallbackQuery, Dict[str, Any]], Awaitable[Any]],
        event: CallbackQuery,
        data: Dict[str, Any],
    ) -> Any:
        session_maker: sessionmaker = data["session_maker"]
        state: FSMContext = data["state"]
        context_data = await state.get_data()
        title = context_data.get("title")
        description = context_data.get("description")
        media = context_data.get("media")
        media_type = context_data.get("media_type")

        async with session_maker() as session:
            async with session.begin():
                try:
                    new_projects_category = ProjectCategoryModel(
                        title=title,
                        description=description,
                        media=media,
                        media_type=media_type,
                    )
                    session.add(new_projects_category)
                    await session.commit()
                    data["result"] = "success"
                except Exception:
                    data["result"] = "fail"
        return await handler(event, data)
