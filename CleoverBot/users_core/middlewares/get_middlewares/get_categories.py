import logging

from db.models.projects_categories import ProjectCategoryModel
from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from sqlalchemy.orm import sessionmaker
from sqlalchemy import select
from sqlalchemy.engine import ScalarResult


class CategoriesPagesMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[CallbackQuery, Dict[str, Any]], Awaitable[Any]],
        event: CallbackQuery,
        data: Dict[str, Any],
    ) -> Any:
        session_maker: sessionmaker = data["session_maker"]
        state: FSMContext = data["state"]
        context_data = await state.get_data()
        try:
            if event.data == "projects":
                new_page = 0
            else:
                page = context_data.get("user_categories_page")
                if "next_categories_page" in event.data:
                    new_page = page + 1
                elif "back_categories_page" in event.data:
                    if page > 0:
                        new_page = page - 1

            async with session_maker() as session:
                async with session.begin():
                    res: ScalarResult = await session.execute(
                        select(ProjectCategoryModel).offset(new_page * 5).limit(5)
                    )
                    categories = res.unique().scalars().all()
                    if categories:
                        categories_dict = {}
                        for category in categories:
                            categories_dict[category.title] = str(category.id)
                        if not new_page:
                            if len(categories) < 5:
                                page = "one"
                            else:
                                page = "first"
                        else:
                            if len(categories) < 5:
                                page = "last"
                            else:
                                page = "middle"
                        data["categories"] = categories_dict
                        data["is_full"] = True
                        data["page"] = page
                        await state.update_data(user_categories_page=new_page)
                    else:
                        data["categories"] = {}
                        data["is_full"] = False
                        data["page"] = ""
                    return await handler(event, data)
        except TypeError as e:
            logging.error(e)
