from users_core.utils.phrases import phrases
from users_core.utils.category_sender import CategorySender
from users_core.keyboards.choise_project_category_keyboard import (
    choise_category_keyboard,
    get_back_from_categories_keyboard,
)
from users_core.keyboards.choise_project_keyboard import choise_project_keyboard
from users_core.middlewares.get_middlewares.get_categories import (
    CategoriesPagesMiddleware,
)
from users_core.middlewares.get_middlewares.get_projects import ProjectsPagesMiddleware
from users_core.middlewares.get_middlewares.get_category_details import (
    CategoryDetailsMiddleware,
)

from db.models.projects_categories import ProjectCategoryModel

from aiogram import Bot, Router, F
from aiogram.types import CallbackQuery, FSInputFile, InputMediaPhoto
from aiogram.fsm.context import FSMContext
from aiogram.exceptions import TelegramBadRequest, TelegramNetworkError


type = "for_user_choise_project"
user_choise_project_category_router = Router()
user_choise_project_router = Router()
user_view_project_router = Router()
user_view_project_category_details_router = Router()


async def show_category_description(
    call: CallbackQuery,
    bot: Bot,
    state: FSMContext,
    category: ProjectCategoryModel | None,
    projects: dict,
    page: str,
    category_id: int,
    is_full: bool,
):
    if category:
        await call.answer()
        sender = CategorySender(category)
        text, media = sender.show_category_for_user()

        if media:
            try:
                await bot.send_media_group(
                    chat_id=call.message.chat.id,
                    media=media,
                )
            except TelegramNetworkError:
                await bot.send_message(chat_id=call.message.chat.id, text=text)
        else:
            await bot.send_message(chat_id=call.message.chat.id, text=text)

        try:
            await call.message.answer(
                text=phrases["choise_project"],
                reply_markup=choise_project_keyboard(
                    projects=projects, page=page, category_id=category_id
                ),
            )
        except TelegramBadRequest:
            await call.answer()
    else:
        await call.message.answer(text="🚫 Can't access the category, try again later!")


async def choise_project_category(
    call: CallbackQuery,
    bot: Bot,
    state: FSMContext,
    categories: dict,
    page: str,
    is_full: bool,
):
    await call.answer()

    media = InputMediaPhoto(
        media=FSInputFile("users_core/utils/photos/categories.png"),
        caption=phrases["choise_project_category"],
    )
    if is_full:
        await call.message.edit_media(
            media=media,
            reply_markup=choise_category_keyboard(
                categories=categories, page=page, type=type
            ),
        )
    else:
        await call.message.edit_media(
            media=media, reply_markup=get_back_from_categories_keyboard()
        )


async def choise_project(
    call: CallbackQuery,
    bot: Bot,
    state: FSMContext,
    projects: dict,
    page: str,
    category_id: int,
    is_full: bool,
):
    try:
        await call.answer()

        if is_full:
            await call.message.edit_text(
                text=phrases["choise_project"],
                reply_markup=choise_project_keyboard(
                    projects=projects, page=page, category_id=category_id
                ),
            )
    except TelegramBadRequest:
        await call.answer()


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

user_view_project_category_details_router.callback_query.register(
    show_category_description, F.data.contains(f"set_project_category_{type}_")
)
user_view_project_category_details_router.callback_query.middleware.register(
    ProjectsPagesMiddleware()
)
user_view_project_category_details_router.callback_query.middleware.register(
    CategoryDetailsMiddleware()
)
