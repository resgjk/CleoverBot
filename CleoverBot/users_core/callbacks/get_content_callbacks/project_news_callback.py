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
from users_core.keyboards.projects_news_keyboard import choise_project_news_keyboard

from db.models.projects import ProjectModel
from db.models.projects_news import ProjectNewsModel

from aiogram import Bot, Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.exceptions import TelegramNetworkError


user_view_project_news_router = Router()
user_view_project_description_router = Router()
user_view_project_news_details_router = Router()


def get_news_text(news):
    text = []
    for one_news in news.keys():
        text.append(f"🔹 {one_news}")
    return f"\n{'-' * 50}\n".join(text)


async def show_project_description(
    call: CallbackQuery,
    bot: Bot,
    state: FSMContext,
    project: ProjectModel | None,
    news: dict,
    page: str,
):
    if project:
        await call.answer()

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
            await bot.send_message(chat_id=call.message.chat.id, text=text)

        text = get_news_text(news)

        await call.message.answer(
            text=text,
            reply_markup=choise_project_news_keyboard(news=news, page=page),
        )
    else:
        await call.message.answer(text="🚫 Can't access the project, try again later!")


async def choise_project_news(
    call: CallbackQuery, bot: Bot, state: FSMContext, news: dict, page: str
):
    await call.answer()

    text = get_news_text(news)

    await call.message.edit_text(
        text=phrases["choise_project_news"] + text,
        reply_markup=choise_project_news_keyboard(news=news, page=page),
    )


async def show_project_news_for_user(
    call: CallbackQuery, bot: Bot, state: FSMContext, news: ProjectNewsModel
):
    await call.answer()

    if news:
        await call.answer()

        sender = NewsSender(news)
        text, media = sender.show_news_to_user()

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
    else:
        await call.message.answer(text="🚫 Can't access the news, try again later!")


user_view_project_description_router.callback_query.register(
    show_project_description, F.data.contains("choise_project_for_user_view_")
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
