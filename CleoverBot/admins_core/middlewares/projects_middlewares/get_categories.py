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
            if event.data in ["add_project", "choise_project"]:
                new_page = 0
                context_data = await state.get_data()
            else:
                page = context_data.get("categories_page")
                if "next_categories_page" in event.data:
                    new_page = page + 1
                elif "back_categories_page" in event.data:
                    if page > 0:
                        new_page = page - 1
                context_data = await state.get_data()

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
                        data["page"] = page
                        data["is_full"] = True
                        await state.update_data(categories_page=new_page)
                    else:
                        data["categories"] = {}
                        data["page"] = ""
                        data["is_full"] = False
                    return await handler(event, data)
        except TypeError:
            pass
