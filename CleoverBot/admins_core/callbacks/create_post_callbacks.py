import asyncio
from uuid import uuid4
from datetime import date, time, timezone
import logging
import re

from users_core.config import scheduler
from admins_core.utils.phrases import phrases
from admins_core.utils.post_form import PostForm
from admins_core.utils.post_sender import PostSender
from admins_core.keyboards.choise_bank_keyboard import get_banks_keyboard
from admins_core.keyboards.choise_category_keyboard import get_activities_keyboard
from admins_core.keyboards.publick_post_keyboard import get_publick_keyboard
from admins_core.middlewares.post_middlewares.get_activities_list import (
    GetActivitiesListMiddleware,
)
from admins_core.middlewares.post_middlewares.get_id_for_send_post import (
    SendPostMiddleware,
)
from admins_core.keyboards.return_to_admin_panel_keyboard import (
    return_to_admin_panel_keyboard,
)

from aiogram import Bot, Router, F
from aiogram.types import (
    CallbackQuery,
    Message,
    ReplyKeyboardRemove,
    ContentType,
    FSInputFile,
)
from aiogram.fsm.context import FSMContext
from aiogram.exceptions import TelegramNetworkError

from apscheduler_di import ContextSchedulerDecorator

from sqlalchemy.orm import sessionmaker


create_post_router = Router()
select_category_router = Router()
send_post_router = Router()

time_pattern = r"^(?:[01]?\d|2[0-3]):[0-5]\d$"
date_pattern = r"^(0[1-9]|[12][0-9]|3[01])\.(0[1-9]|1[0-2])\.\d{4}$"


async def create_post(call: CallbackQuery, bot: Bot, state: FSMContext):
    await call.answer()
    await call.message.answer(text=phrases["input_title"])
    await state.set_state(PostForm.GET_TITLE)
    await state.update_data(owner_id=call.from_user.id)


async def get_title(message: Message, bot: Bot, state: FSMContext, activities: dict):
    if message.content_type == ContentType.TEXT:
        await message.answer(
            text=phrases["choise_categoty"],
            reply_markup=get_activities_keyboard(activities),
        )
        await state.update_data(title=message.text)
        await state.set_state(PostForm.GET_CATEGORY)
    else:
        await message.answer(
            text="Введите название в верном формате:",
        )


async def get_category(message: Message, bot: Bot, state: FSMContext):
    await message.answer(text=phrases["choise_bank"], reply_markup=get_banks_keyboard())
    await state.update_data(category=int(message.text.split(" | ")[0]))
    await state.set_state(PostForm.GET_BANK)


async def get_bank(message: Message, bot: Bot, state: FSMContext):
    await message.answer(
        text=phrases["input_start_date"], reply_markup=ReplyKeyboardRemove()
    )
    await state.update_data(bank=message.text)
    await state.set_state(PostForm.GET_START_DATE)


async def get_start_date(message: Message, bot: Bot, state: FSMContext):
    if message.text == "-":
        await message.answer(phrases["input_end_date"])
        await state.update_data(start_date=None)
        await state.update_data(start_time=None)
        await state.set_state(PostForm.GET_END_DATE)
    else:
        if re.match(date_pattern, message.text):
            str_date = message.text.split(".")
            await message.answer(phrases["input_start_time"])
            valid_date = date(
                year=int(str_date[2]), month=int(str_date[1]), day=int(str_date[0])
            )
            await state.update_data(start_date=valid_date.isoformat())
            await state.set_state(PostForm.GET_START_TIME)
        else:
            await message.answer(
                text="Неверный формат даты. Введите дату еще раз в формате дд.мм.гггг UTC"
            )


async def get_start_time(message: Message, bot: Bot, state: FSMContext):
    if message.text == "-":
        await message.answer(phrases["input_end_date"])
        await state.set_state(PostForm.GET_END_DATE)
    else:
        if re.match(time_pattern, message.text):
            str_time = message.text.split(":")
            await message.answer(phrases["input_end_date"])
            valid_time = time(
                hour=int(str_time[0]), minute=int(str_time[1]), tzinfo=timezone.utc
            )
            await state.update_data(start_time=valid_time.isoformat())
            await state.set_state(PostForm.GET_END_DATE)
        else:
            await message.answer(
                text="Неверный формат времени. Введите время еще раз в формате чч.мм UTC"
            )


async def get_end_date(message: Message, bot: Bot, state: FSMContext):
    if message.text == "-":
        await message.answer(phrases["input_short_description"])
        await state.update_data(end_date=None)
        await state.update_data(end_time=None)
        await state.set_state(PostForm.GET_SHORT_DESCRIPTION)
    else:
        if re.match(date_pattern, message.text):
            str_date = message.text.split(".")
            await message.answer(phrases["input_end_time"])
            valid_date = date(
                year=int(str_date[2]), month=int(str_date[1]), day=int(str_date[0])
            )
            await state.update_data(end_date=valid_date.isoformat())
            await state.set_state(PostForm.GET_END_TIME)
        else:
            await message.answer(
                text="Неверный формат даты. Введите дату еще раз в формате дд.мм.гггг UTC"
            )


async def get_end_time(message: Message, bot: Bot, state: FSMContext):
    if message.text == "-":
        await message.answer(phrases["input_short_description"])
        await state.set_state(PostForm.GET_SHORT_DESCRIPTION)
    else:
        if re.match(time_pattern, message.text):
            str_time = message.text.split(":")
            await message.answer(phrases["input_short_description"])
            valid_time = time(
                hour=int(str_time[0]), minute=int(str_time[1]), tzinfo=timezone.utc
            )
            await state.update_data(end_time=valid_time.isoformat())
            await state.set_state(PostForm.GET_SHORT_DESCRIPTION)
        else:
            await message.answer(
                text="Неверный формат времени. Введите время еще раз в формате чч.мм UTC"
            )


async def get_short_description(message: Message, bot: Bot, state: FSMContext):
    if message.content_type == ContentType.TEXT:
        await message.answer(text=phrases["input_full_description"])
        await state.update_data(short_description=message.text, post_uuid=str(uuid4()))
        await state.set_state(PostForm.GET_FULL_DESCRIPTION)
    else:
        await message.answer(
            text="Введите краткое описание в верном формате:",
        )


async def get_full_description(message: Message, bot: Bot, state: FSMContext):
    if message.content_type == ContentType.TEXT:
        await message.answer(text=phrases["input_media"])
        await state.update_data(full_description=message.html_text)
        await state.set_state(PostForm.GET_MEDIA_FILES)
    else:
        await message.answer(
            text="Введите полное описание в верном формате:",
        )


async def get_media_files(message: Message, bot: Bot, state: FSMContext):
    context_data = await state.get_data()
    post_uuid = context_data.get("post_uuid")
    if message.content_type == ContentType.PHOTO:
        file = await bot.get_file(message.photo[-1].file_id)
        photo_title = f"media/posts_media/photos/{post_uuid}.jpg"
        await state.update_data(media=photo_title, media_type="photo")
        await bot.download_file(file.file_path, photo_title)
        await state.set_state(PostForm.SAVE_MEDIA_AND_SHOW_POST)
    elif message.content_type == ContentType.VIDEO:
        file = await bot.get_file(message.video.file_id)
        video_title = f"media/posts_media/videos/{post_uuid}.mp4"
        await state.update_data(media=video_title, media_type="video")
        await bot.download_file(file.file_path, video_title)
        await state.set_state(PostForm.SAVE_MEDIA_AND_SHOW_POST)
    elif message.content_type == ContentType.TEXT and message.text == "-":
        await state.update_data(media=None, media_type=None)
        await state.set_state(PostForm.SAVE_MEDIA_AND_SHOW_POST)

    state_type = await state.get_state()
    if state_type == PostForm.SAVE_MEDIA_AND_SHOW_POST:
        context_data = await state.get_data()
        sender = PostSender(context_data=context_data)

        text, media = sender.show_post_detail_for_admin()
        media_type = context_data.get("media_type")

        if media:
            try:
                if media_type == "photo":
                    await bot.send_photo(
                        chat_id=message.chat.id, photo=media, caption=text
                    )
                elif media_type == "video":
                    await bot.send_video(
                        chat_id=message.chat.id, video=media, caption=text
                    )
            except TelegramNetworkError:
                event_photo = FSInputFile("users_core/utils/photos/event.png")
                await bot.send_photo(
                    chat_id=message.chat.id, photo=event_photo, caption=text
                )
        else:
            event_photo = FSInputFile("users_core/utils/photos/event.png")
            await bot.send_photo(
                chat_id=message.chat.id, photo=event_photo, caption=text
            )

        await bot.send_message(
            text=phrases["finish_message"],
            chat_id=message.chat.id,
            reply_markup=get_publick_keyboard(),
        )
        await state.set_state(PostForm.SEND_POST_TO_USERS)


async def send_post_to_users(
    call: CallbackQuery,
    bot: Bot,
    state: FSMContext,
    users_id: list,
    scheduler: ContextSchedulerDecorator,
    session_maker: sessionmaker,
):
    await call.answer()
    context_data = await state.get_data()
    sender = PostSender(context_data=context_data)

    if users_id:
        text, media = sender.send_post_to_users(scheduler=scheduler)
        media_type = context_data.get("media_type")

        tasks = []
        try:
            for id in users_id:
                if media:
                    try:
                        if media_type == "photo":
                            task = bot.send_photo(chat_id=id, photo=media, caption=text)
                        elif media_type == "video":
                            task = bot.send_video(chat_id=id, video=media, caption=text)
                    except TelegramNetworkError:
                        event_photo = FSInputFile("users_core/utils/photos/event.png")
                        task = bot.send_photo(
                            chat_id=id, photo=event_photo, caption=text
                        )
                else:
                    event_photo = FSInputFile("users_core/utils/photos/event.png")
                    task = bot.send_photo(chat_id=id, photo=event_photo, caption=text)
                tasks.append(task)
            for success_task in tasks:
                await success_task
                await asyncio.sleep(0.04)
            await state.clear()
            await call.message.edit_text(
                text="✅ Пост успешно опубликован!",
                reply_markup=return_to_admin_panel_keyboard(),
            )
        except Exception as e:
            logging.error(e)
            await call.message.answer(
                text=f"Не удалось опубликовать пост, попробуйте еще раз!\nОшибка: {str(e)}"
            )
    else:
        await call.message.edit_text(
            text="✅ Пост успешно опубликован!",
            reply_markup=return_to_admin_panel_keyboard(),
        )
    await state.clear()


create_post_router.callback_query.register(create_post, F.data == "create_post")
select_category_router.message.register(get_title, PostForm.GET_TITLE)
select_category_router.message.middleware.register(GetActivitiesListMiddleware())
create_post_router.message.register(get_category, PostForm.GET_CATEGORY)
create_post_router.message.register(get_bank, PostForm.GET_BANK)
create_post_router.message.register(get_start_date, PostForm.GET_START_DATE)
create_post_router.message.register(get_start_time, PostForm.GET_START_TIME)
create_post_router.message.register(get_end_date, PostForm.GET_END_DATE)
create_post_router.message.register(get_end_time, PostForm.GET_END_TIME)
create_post_router.message.register(
    get_short_description, PostForm.GET_SHORT_DESCRIPTION
)
create_post_router.message.register(get_full_description, PostForm.GET_FULL_DESCRIPTION)
create_post_router.message.register(get_media_files, PostForm.GET_MEDIA_FILES)
send_post_router.callback_query.register(
    send_post_to_users, F.data == "publick_post", PostForm.SEND_POST_TO_USERS
)
send_post_router.callback_query.middleware.register(SendPostMiddleware(scheduler))
