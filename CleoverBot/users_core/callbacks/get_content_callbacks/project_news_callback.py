import logging

from users_core.utils.phrases import phrases
from users_core.utils.project_sender import ProjectSender
from users_core.utils.project_news_sender import NewsSender
from users_core.middlewares.get_middlewares.get_projects_news import (
    ProjectsNewsPagesMiddleware,
)
from users_core.middlewares.get_middlewares.get_project_details import (
    ProjectDetailsMiddleware,
)
from users_core.middlewares.get_middlewares.get_project_news_details import (
    NewsDetailsMiddleware,
)
from users_core.keyboards.projects_news_keyboard import (
    choise_project_news_keyboard,
    return_to_project_keyboard,
)

from db.models.projects import ProjectModel
from db.models.projects_news import ProjectNewsModel

from aiogram import Bot, Router, F
from aiogram.types import CallbackQuery, FSInputFile
from aiogram.fsm.context import FSMContext
from aiogram.exceptions import TelegramNetworkError


user_view_project_news_router = Router()
user_view_project_description_router = Router()
user_view_project_news_details_router = Router()


async def show_project_description(
    call: CallbackQuery,
    bot: Bot,
    state: FSMContext,
    project: ProjectModel | None,
    news: dict,
    page: str,
):
    await call.answer()

    context_data = await state.get_data()
    chat_id = call.message.chat.id
    message_ids_for_delete = []
    if "return_to_project_" in call.data:
        for message_number in range(int(call.data.split("_")[-2])):
            message_ids_for_delete.append(call.message.message_id - message_number)
    else:
        message_counte = context_data.get("category_media_count") + 1
        for message_number in range(message_counte):
            message_ids_for_delete.append(call.message.message_id - message_number)
    try:
        await bot.delete_messages(chat_id=chat_id, message_ids=message_ids_for_delete)
    except Exception as e:
        logging.error(e)

    if project:
        sender = ProjectSender(project)
        text, media = sender.show_project_details()

        if media:
            try:
                await bot.send_media_group(
                    chat_id=call.message.chat.id,
                    media=media,
                )
            except TelegramNetworkError:
                await bot.send_message(chat_id=call.message.chat.id, text=text)
        else:
            project_photo = FSInputFile("users_core/utils/photos/project.png")
            await bot.send_photo(
                chat_id=call.message.chat.id, photo=project_photo, caption=text
            )

        await call.message.answer(
            text=phrases["choise_project_news"],
            reply_markup=choise_project_news_keyboard(
                news=news,
                page=page,
                media_count=len(media),
                category_id=context_data.get("category_id"),
            ),
        )
        await state.update_data(
            project_media_count=len(media), project_id=int(call.data.split("_")[-1])
        )
    else:
        await call.message.answer(text="🚫 Can't access the project, try again later!")


async def choise_project_news(
    call: CallbackQuery,
    bot: Bot,
    state: FSMContext,
    news: dict,
    page: str,
    is_full: bool,
):
    await call.answer()

    if is_full:
        context_data = await state.get_data()
        await call.message.edit_text(
            text=phrases["choise_project_news"],
            reply_markup=choise_project_news_keyboard(
                news=news,
                page=page,
                media_count=context_data.get("project_media_count"),
                category_id=context_data.get("category_id"),
            ),
        )


async def show_project_news_for_user(
    call: CallbackQuery, bot: Bot, state: FSMContext, news: ProjectNewsModel
):
    await call.answer()
    context_data = await state.get_data()
    chat_id = call.message.chat.id

    message_ids_for_delete = []
    message_counte = context_data.get("project_media_count") + 1
    for message_number in range(message_counte):
        message_ids_for_delete.append(call.message.message_id - message_number)

    try:
        await bot.delete_messages(chat_id=chat_id, message_ids=message_ids_for_delete)
    except Exception as e:
        logging.error(e)

    if news:
        sender = NewsSender(news)
        text, media = sender.show_news_to_user()
        project_id = context_data.get("project_id")

        if media:
            try:
                await bot.send_media_group(
                    chat_id=call.message.chat.id,
                    media=media,
                )
                await bot.send_message(
                    chat_id=call.message.chat.id,
                    text=text,
                    reply_markup=return_to_project_keyboard(
                        media_count=len(media), project_id=project_id
                    ),
                )
            except TelegramNetworkError:
                await bot.send_message(
                    chat_id=call.message.chat.id,
                    text=text,
                    reply_markup=return_to_project_keyboard(
                        media_count=0, project_id=project_id
                    ),
                )
        else:
            news_photo = FSInputFile("users_core/utils/photos/news.png")
            await bot.send_photo(
                chat_id=call.message.chat.id,
                photo=news_photo,
                caption=text,
                reply_markup=return_to_project_keyboard(
                    media_count=len(media), project_id=project_id
                ),
            )
    else:
        await call.message.answer(text="🚫 Can't access the news, try again later!")


user_view_project_description_router.callback_query.register(
    show_project_description, F.data.contains("choise_project_for_user_view_")
)
user_view_project_description_router.callback_query.register(
    show_project_description, F.data.contains("return_to_project")
)
user_view_project_description_router.callback_query.middleware.register(
    ProjectsNewsPagesMiddleware()
)
user_view_project_description_router.callback_query.middleware.register(
    ProjectDetailsMiddleware()
)

user_view_project_news_router.callback_query.register(
    choise_project_news, F.data == "next_project_news_page"
)
user_view_project_news_router.callback_query.register(
    choise_project_news, F.data == "back_project_news_page"
)
user_view_project_news_router.callback_query.middleware.register(
    ProjectsNewsPagesMiddleware()
)

user_view_project_news_details_router.callback_query.register(
    show_project_news_for_user, F.data.contains("view_project_news_")
)
user_view_project_news_details_router.callback_query.middleware.register(
    NewsDetailsMiddleware()
)
