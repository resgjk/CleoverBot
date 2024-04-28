from admins_core.utils.phrases import phrases
from admins_core.utils.project_sender import ProjectSender
from admins_core.keyboards.choise_project_category_keyboard import (
    choise_category_keyboard,
)
from admins_core.keyboards.project_route_keyboard import get_project_route_keyboard
from admins_core.keyboards.choise_project_keyboard import choise_project_keyboard
from admins_core.middlewares.projects_middlewares.get_categories import (
    CategoriesPagesMiddleware,
)
from admins_core.middlewares.projects_middlewares.get_projects import (
    ProjectsPagesMiddleware,
)
from admins_core.middlewares.projects_middlewares.get_project_data import (
    ProjectDetailsMiddleware,
)

from aiogram import Bot, Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext


type = "for_choise_project"
choise_project_category_router = Router()
choise_project_router = Router()
view_project_router = Router()


async def choise_project_category(
    call: CallbackQuery, bot: Bot, state: FSMContext, categories: dict, page: str
):
    await call.message.edit_text(
        text=phrases["choise_project_category"],
        reply_markup=choise_category_keyboard(
            categories=categories, page=page, type=type
        ),
    )


async def choise_project(
    call: CallbackQuery, bot: Bot, state: FSMContext, projects: dict, page: str
):
    await call.message.edit_text(
        text=phrases["choise_project"],
        reply_markup=choise_project_keyboard(projects=projects, page=page),
    )


async def view_project(
    call: CallbackQuery, bot: Bot, state: FSMContext, project_data: dict, result: str
):
    await call.answer()

    if result == "success":
        sender = ProjectSender(project_data=project_data)
        text, media = sender.show_for_add_news_or_delete()

        if media:
            await bot.send_media_group(
                chat_id=call.message.chat.id,
                media=media,
            )
        else:
            await call.message.answer(
                text=text,
            )
        await bot.send_message(
            text="👇 Выберите действие:",
            chat_id=call.message.chat.id,
            reply_markup=get_project_route_keyboard(project_data["id"]),
        )
    else:
        await call.message.answer(
            text="Не удалось выбрать данный проект, попробуйте еще раз!"
        )


choise_project_category_router.callback_query.register(
    choise_project_category, F.data == "choise_project"
)
choise_project_category_router.callback_query.register(
    choise_project_category, F.data == f"next_categories_page_{type}"
)
choise_project_category_router.callback_query.register(
    choise_project_category, F.data == f"back_categories_page_{type}"
)
choise_project_category_router.callback_query.middleware.register(
    CategoriesPagesMiddleware()
)

choise_project_router.callback_query.register(
    choise_project, F.data.contains(f"set_project_category_{type}_")
)
choise_project_router.callback_query.register(
    choise_project, F.data == "next_projects_page"
)
choise_project_router.callback_query.register(
    choise_project, F.data == "back_projects_page"
)
choise_project_router.callback_query.middleware.register(ProjectsPagesMiddleware())

view_project_router.callback_query.register(
    view_project, F.data.contains("choise_project_for_view")
)
view_project_router.callback_query.middleware.register(ProjectDetailsMiddleware())
