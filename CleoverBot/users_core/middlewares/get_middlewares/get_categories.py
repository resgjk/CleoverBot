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
                await state.update_data(user_categories_page=1)
                context_data = await state.get_data()
            else:
                page = context_data.get("user_categories_page")
                if "next_categories_page" in event.data:
                    new_page = page + 1
                elif "back_categories_page" in event.data:
                    new_page = page - 1
                await state.update_data(user_categories_page=new_page)
                context_data = await state.get_data()

            async with session_maker() as session:
                async with session.begin():
                    categories_page = context_data.get("user_categories_page")
                    res: ScalarResult = await session.execute(
                        select(ProjectCategoryModel)
                    )
                    categories = res.unique().scalars().all()
                    categories_dict = {}
                    if len(categories) <= 5:
                        for category in categories:
                            categories_dict[category.title] = str(category.id)
                        page = "one"
                    elif categories_page == 1:
                        for category in categories[:5]:
                            categories_dict[category.title] = str(category.id)
                        page = "first"
                    else:
                        if 5 * categories_page == len(categories):
                            for category in categories[-5:]:
                                categories_dict[category.title] = str(category.id)
                            page = "last"
                        elif 5 * categories_page < len(categories):
                            for category in categories[
                                (5 * categories_page) - 5 : (5 * categories_page)
                            ]:
                                categories_dict[category.title] = str(category.id)
                            page = "middle"
                        elif (
                            5 * categories_page > len(categories)
                            and 5 * categories_page - len(categories) < 5
                        ):
                            for category in categories[(5 * (categories_page - 1)) :]:
                                categories_dict[category.title] = str(category.id)
                            page = "last"
                    data["categories"] = categories_dict
                    data["page"] = page
                    return await handler(event, data)
        except TypeError:
            pass
