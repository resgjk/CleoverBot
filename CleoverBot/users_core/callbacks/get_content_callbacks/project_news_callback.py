from users_core.utils.phrases import phrases
from users_core.utils.project_sender import ProjectSender
from users_core.utils.project_news_sender import NewsSender
from users_core.keyboards.return_to_main_keyboard import get_keyboard
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
from aiogram.types import CallbackQuery, FSInputFile, InputMediaPhoto, InputMediaVideo
from aiogram.fsm.context import FSMContext
from aiogram.exceptions import TelegramBadRequest, TelegramNetworkError


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

    if project:
        sender = ProjectSender(project)
        text, media = sender.show_project_details()
        media_type = project.media_type

        try:
            if media:
                try:
                    if media_type == "photo":
                        message_media = InputMediaPhoto(
                            media=media, caption=(text + phrases["choise_project_news"])
                        )
                        await call.message.edit_media(
                            media=message_media,
                            reply_markup=choise_project_news_keyboard(
                                news=news,
                                page=page,
                                category_id=context_data.get("category_id"),
                            ),
                        )
                    elif media_type == "video":
                        message_media = InputMediaVideo(
                            media=media, caption=(text + phrases["choise_project_news"])
                        )
                        await call.message.edit_media(
                            media=message_media,
                            reply_markup=choise_project_news_keyboard(
                                news=news,
                                page=page,
                                category_id=context_data.get("category_id"),
                            ),
                        )
                except TelegramNetworkError:
                    project_photo = FSInputFile("users_core/utils/photos/project.png")
                    project_message_media = InputMediaPhoto(
                        media=project_photo,
                        caption=(text + phrases["choise_project_news"]),
                    )
                    await call.message.edit_media(
                        media=project_message_media,
                        reply_markup=choise_project_news_keyboard(
                            news=news,
                            page=page,
                            category_id=context_data.get("category_id"),
                        ),
                    )
            else:
                project_photo = FSInputFile("users_core/utils/photos/project.png")
                project_message_media = InputMediaPhoto(
                    media=project_photo, caption=(text + phrases["choise_project_news"])
                )
                await call.message.edit_media(
                    media=project_message_media,
                    reply_markup=choise_project_news_keyboard(
                        news=news,
                        page=page,
                        category_id=context_data.get("category_id"),
                    ),
                )
            await state.update_data(project_id=int(call.data.split("_")[-1]))
        except TelegramBadRequest:
            await call.message.edit_caption(
                caption="🚫 Can't access the project, try again later!",
                reply_markup=get_keyboard(),
            )
    else:
        await call.message.edit_caption(
            caption="🚫 Can't access the project, try again later!",
            reply_markup=get_keyboard(),
        )


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
        await call.message.edit_reply_markup(
            reply_markup=choise_project_news_keyboard(
                news=news,
                page=page,
                category_id=context_data.get("category_id"),
            ),
        )


async def show_project_news_for_user(
    call: CallbackQuery, bot: Bot, state: FSMContext, news: ProjectNewsModel
):
    await call.answer()
    context_data = await state.get_data()

    if news:
        sender = NewsSender(news)
        text, media = sender.show_news_to_user()
        media_type = news.media_type
        project_id = context_data.get("project_id")

        try:
            if media:
                try:
                    if media_type == "photo":
                        message_media = InputMediaPhoto(media=media, caption=text)
                        await call.message.edit_media(
                            media=message_media,
                            reply_markup=return_to_project_keyboard(
                                project_id=project_id
                            ),
                        )
                    elif media_type == "video":
                        message_media = InputMediaVideo(media=media, caption=text)
                        await call.message.edit_media(
                            media=message_media,
                            reply_markup=return_to_project_keyboard(
                                project_id=project_id
                            ),
                        )
                except TelegramNetworkError:
                    news_photo = FSInputFile("users_core/utils/photos/news.png")
                    news_message_media = InputMediaPhoto(
                        media=news_photo,
                        caption=text,
                    )
                    await call.message.edit_media(
                        media=news_message_media,
                        reply_markup=return_to_project_keyboard(project_id=project_id),
                    )
            else:
                news_photo = FSInputFile("users_core/utils/photos/news.png")
                news_message_media = InputMediaPhoto(
                    media=news_photo,
                    caption=text,
                )
                await call.message.edit_media(
                    media=news_message_media,
                    reply_markup=return_to_project_keyboard(project_id=project_id),
                )
        except TelegramBadRequest:
            await call.message.edit_caption(
                caption="🚫 Can't access the news, try again later!",
                reply_markup=get_keyboard(),
            )
    else:
        await call.message.edit_caption(
            caption="🚫 Can't access the news, try again later!",
            reply_markup=get_keyboard(),
        )


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
