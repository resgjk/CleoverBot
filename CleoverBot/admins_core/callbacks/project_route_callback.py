from admins_core.utils.phrases import phrases
from admins_core.utils.news_form import NewsForm
from admins_core.utils.news_sender import NewsSender
from admins_core.keyboards.return_to_projects_settings import (
    return_to_projects_settings_keyboard,
)
from admins_core.keyboards.return_to_project_route_menu import (
    return_to_project_route_menu_keyboard,
)
from admins_core.keyboards.publick_project_news_keyboard import get_publick_keyboard
from admins_core.keyboards.save_project_news_media_keyboard import get_media_keyboard
from admins_core.middlewares.projects_middlewares.delete_project_middlewares import (
    DeleteProjectMiddleware,
)
from admins_core.middlewares.projects_middlewares.get_id_for_send_project_news import (
    SendNewsMiddleware,
)
from admins_core.middlewares.check_middlewares.check_project import (
    CheckProjectForAddNewsMiddleware,
)

from uuid import uuid4
import asyncio

from aiogram import Bot, Router, F
from aiogram.types import CallbackQuery, Message, ContentType
from aiogram.fsm.context import FSMContext
from aiogram.exceptions import TelegramNetworkError


delete_project_router = Router()
check_project_router = Router()
add_project_news_router = Router()
send_project_news_router = Router()


async def delete_project(call: CallbackQuery, bot: Bot, result: str):
    if result == "success":
        await call.message.edit_text(
            text=phrases["success_project_delete"],
            reply_markup=return_to_projects_settings_keyboard(),
        )
    elif result == "error":
        await call.message.edit_text(
            text=phrases["error_project_delete"],
            reply_markup=return_to_projects_settings_keyboard(),
        )
    elif result == "was_deleted":
        await call.message.edit_text(
            text=phrases["was_deleted_project_delete"],
            reply_markup=return_to_projects_settings_keyboard(),
        )


async def add_project_news(
    call: CallbackQuery, bot: Bot, state: FSMContext, result: str
):
    if result == "success":
        await call.answer()
        await call.message.answer(text=phrases["input_news_title"])
        await state.set_state(NewsForm.GET_TITLE)
        await state.update_data(
            project_news_id=int(call.data.split("_")[-1]), owner_id=call.from_user.id
        )
    else:
        await call.message.edit_text(
            text=phrases["project_isnt_in_db"],
            reply_markup=return_to_projects_settings_keyboard(),
        )


async def get_news_title(message: Message, bot: Bot, state: FSMContext):
    await message.answer(text=phrases["input_news_description"])
    await state.set_state(NewsForm.GET_DESCRIPTION)
    await state.update_data(title=message.text)


async def get_news_description(message: Message, bot: Bot, state: FSMContext):
    await message.answer(
        text=phrases["input_news_media"], reply_markup=get_media_keyboard()
    )
    await state.update_data(
        description=message.html_text, news_uuid=str(uuid4()), photos="", videos=""
    )
    await state.set_state(NewsForm.GET_MEDIA_FILES)


async def get_media_files(message: Message, bot: Bot, state: FSMContext):
    context_data = await state.get_data()
    news_uuid = context_data.get("news_uuid")
    photos = context_data.get("photos")
    videos = context_data.get("videos")
    if message.content_type == ContentType.PHOTO:
        file = await bot.get_file(message.photo[-1].file_id)
        photo_title = f"media/projects_media/news/photos/{news_uuid}_photo_{len(photos.split(';')) - 1}.jpg"
        photos += photo_title + ";"
        await state.update_data(photos=photos)
        await bot.download_file(file.file_path, photo_title)
    elif message.content_type == ContentType.VIDEO:
        file = await bot.get_file(message.video.file_id)
        video_title = f"media/projects_media/news/videos/{news_uuid}_video_{len(videos.split(';')) - 1}.mp4"
        videos += video_title + ";"
        await state.update_data(videos=videos)
        await bot.download_file(file.file_path, video_title)


async def save_media_and_show_news(call: CallbackQuery, bot: Bot, state: FSMContext):
    await call.answer()

    context_data = await state.get_data()
    sender = NewsSender(context_data=context_data)

    text, media = sender.show_news_detail_for_admin()

    if media:
        try:
            await bot.send_media_group(
                chat_id=call.message.chat.id,
                media=media,
            )
        except TelegramNetworkError:
            await call.message.answer(text=text)
    else:
        await call.message.answer(text=text)
    await bot.send_message(
        text=phrases["finish_news_message"],
        chat_id=call.message.chat.id,
        reply_markup=get_publick_keyboard(context_data.get("project_news_id")),
    )
    await state.set_state(NewsForm.SEND_NEWS_TO_USERS)


async def send_post_to_users(
    call: CallbackQuery,
    bot: Bot,
    state: FSMContext,
    users_id: list,
):
    await call.answer()
    context_data = await state.get_data()
    sender = NewsSender(context_data=context_data)

    if users_id:
        text, media = sender.send_news_to_users()

        tasks = []
        try:
            for id in users_id:
                if media:
                    try:
                        task = bot.send_media_group(
                            chat_id=id,
                            media=media,
                        )
                    except TelegramNetworkError:
                        task = bot.send_message(chat_id=id, text=text)
                else:
                    task = bot.send_message(chat_id=id, text=text)
                tasks.append(task)
            await asyncio.gather(*tasks, return_exceptions=True)
            await state.clear()
            await call.message.edit_text(
                text="✅ Новость успешно опубликована!",
                reply_markup=return_to_project_route_menu_keyboard(
                    context_data.get("project_news_id")
                ),
            )
        except Exception:
            await call.message.answer(
                text="Не удалось опубликовать новость, попробуйте еще раз!"
            )
    else:
        await call.message.edit_text(
            text="✅ Новость успешно опубликована!",
            reply_markup=return_to_project_route_menu_keyboard(
                context_data.get("project_news_id")
            ),
        )
    await state.clear()


delete_project_router.callback_query.register(
    delete_project, F.data.contains("delete_project_")
)
delete_project_router.callback_query.middleware.register(DeleteProjectMiddleware())

check_project_router.callback_query.register(
    add_project_news, F.data.contains("add_news_for_project_")
)
check_project_router.callback_query.middleware.register(
    CheckProjectForAddNewsMiddleware()
)
add_project_news_router.message.register(get_news_title, NewsForm.GET_TITLE)
add_project_news_router.message.register(get_news_description, NewsForm.GET_DESCRIPTION)
add_project_news_router.message.register(get_media_files, NewsForm.GET_MEDIA_FILES)
add_project_news_router.callback_query.register(
    save_media_and_show_news,
    F.data == "save_project_news_media",
    NewsForm.GET_MEDIA_FILES,
)

send_project_news_router.callback_query.register(
    send_post_to_users, F.data == "publick_project_news", NewsForm.SEND_NEWS_TO_USERS
)
send_project_news_router.callback_query.middleware.register(SendNewsMiddleware())