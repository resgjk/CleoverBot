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
from aiogram.types import CallbackQuery, FSInputFile
from aiogram.fsm.context import FSMContext
from aiogram.exceptions import TelegramNetworkError


type = "for_choise_project"
choise_project_category_router = Router()
choise_project_router = Router()
view_project_router = Router()


async def choise_project_category(
    call: CallbackQuery,
    bot: Bot,
    state: FSMContext,
    categories: dict,
    page: str,
    is_full: bool,
):
    await call.answer()
    if is_full:
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
    is_full: bool,
):
    await call.answer()

    if is_full:
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
        text, media = sender.send_project()
        media_type = project_data["media_type"]

        if media:
            try:
                if media_type == "photo":
                    await bot.send_photo(
                        chat_id=call.from_user.id,
                        photo=media,
                        caption=text,
                        reply_markup=get_project_route_keyboard(project_data["id"]),
                    )
                elif media_type == "video":
                    await bot.send_video(
                        chat_id=call.from_user.id,
                        video=media,
                        caption=text,
                        reply_markup=get_project_route_keyboard(project_data["id"]),
                    )
            except TelegramNetworkError:
                project_photo = FSInputFile("users_core/utils/photos/project.png")
                await bot.send_photo(
                    chat_id=call.from_user.id,
                    photo=project_photo,
                    caption=text,
                    reply_markup=get_project_route_keyboard(project_data["id"]),
                )
        else:
            project_photo = FSInputFile("users_core/utils/photos/project.png")
            await bot.send_photo(
                chat_id=call.from_user.id,
                photo=project_photo,
                caption=text,
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
