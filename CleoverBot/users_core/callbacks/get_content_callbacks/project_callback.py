from users_core.utils.phrases import phrases
from users_core.keyboards.choise_project_category_keyboard import (
    choise_category_keyboard,
)
from users_core.middlewares.get_middlewares.get_categories import (
    CategoriesPagesMiddleware,
)

from aiogram import Bot, Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext


type = "for_user_choise_project"
user_choise_project_category_router = Router()
user_choise_project_router = Router()
user_view_project_router = Router()


async def choise_project_category(
    call: CallbackQuery, bot: Bot, state: FSMContext, categories: dict, page: str
):
    await call.answer()
    await call.message.edit_text(
        text=phrases["choise_project_category"],
        reply_markup=choise_category_keyboard(
            categories=categories, page=page, type=type
        ),
    )


user_choise_project_category_router.callback_query.register(
    choise_project_category, F.data == "projects"
)
user_choise_project_category_router.callback_query.register(
    choise_project_category, F.data == f"next_categories_page_{type}"
)
user_choise_project_category_router.callback_query.register(
    choise_project_category, F.data == f"back_categories_page_{type}"
)
user_choise_project_category_router.callback_query.middleware.register(
    CategoriesPagesMiddleware()
)
