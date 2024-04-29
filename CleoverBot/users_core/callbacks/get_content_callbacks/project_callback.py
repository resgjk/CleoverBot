from users_core.utils.phrases import phrases
from users_core.keyboards.choise_project_category_keyboard import (
    choise_category_keyboard,
)
from users_core.keyboards.choise_project_keyboard import choise_project_keyboard
from users_core.middlewares.get_middlewares.get_categories import (
    CategoriesPagesMiddleware,
)
from users_core.middlewares.get_middlewares.get_projects import ProjectsPagesMiddleware

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


async def choise_project(
    call: CallbackQuery,
    bot: Bot,
    state: FSMContext,
    projects: dict,
    page: str,
    category_id: int,
):
    await call.message.edit_text(
        text=phrases["choise_project"],
        reply_markup=choise_project_keyboard(
            projects=projects, page=page, category_id=category_id
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

user_choise_project_router.callback_query.register(
    choise_project, F.data.contains("_project_notification_for_user_")
)
user_choise_project_router.callback_query.register(
    choise_project, F.data.contains(f"set_project_category_{type}_")
)
user_choise_project_router.callback_query.register(
    choise_project, F.data.contains("next_projects_page_for_user_choise_project")
)
user_choise_project_router.callback_query.register(
    choise_project, F.data.contains("back_projects_page_for_user_choise_project")
)
user_choise_project_router.callback_query.register(
    choise_project, F.data.contains("enable_notifications_category_")
)
user_choise_project_router.callback_query.register(
    choise_project, F.data.contains("turn_off_notifications_category_")
)
user_choise_project_router.callback_query.middleware.register(ProjectsPagesMiddleware())
