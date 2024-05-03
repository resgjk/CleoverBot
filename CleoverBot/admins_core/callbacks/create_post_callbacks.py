import asyncio
from uuid import uuid4

from users_core.config import scheduler
from admins_core.utils.phrases import phrases
from admins_core.utils.post_form import PostForm
from admins_core.utils.post_sender import PostSender
from admins_core.keyboards.choise_bank_keyboard import get_banks_keyboard
from admins_core.keyboards.choise_category_keyboard import get_activities_keyboard
from admins_core.keyboards.finish_create_post_keyboard import get_media_keyboard
from admins_core.keyboards.publick_post_keyboard import get_publick_keyboard
from admins_core.middlewares.post_middlewares.get_id_for_send_post import (
    SendPostMiddleware,
)
from admins_core.keyboards.return_to_admin_panel_keyboard import (
    return_to_admin_panel_keyboard,
)

from aiogram import Bot, Router, F
from aiogram.types import CallbackQuery, Message, ReplyKeyboardRemove, ContentType
from aiogram.fsm.context import FSMContext
from aiogram.exceptions import TelegramNetworkError

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from sqlalchemy.orm import sessionmaker


create_post_router = Router()
send_post_router = Router()


async def create_post(call: CallbackQuery, bot: Bot, state: FSMContext):
    await call.answer()
    await call.message.answer(text=phrases["input_title"])
    await state.set_state(PostForm.GET_TITLE)
    await state.update_data(owner_id=call.from_user.id)


async def get_title(message: Message, bot: Bot, state: FSMContext):
    await message.answer(
        text=phrases["choise_categoty"], reply_markup=get_activities_keyboard()
    )
    await state.update_data(title=message.text, photos="", videos="")
    await state.set_state(PostForm.GET_CATEGORY)


async def get_category(message: Message, bot: Bot, state: FSMContext):
    await message.answer(text=phrases["choise_bank"], reply_markup=get_banks_keyboard())
    match message.text:
        case "DeFi 📚":
            category = "defi"
        case "Airdrops 💸":
            category = "airdrops"
        case "News 🗞":
            category = "news"
        case "IDO | ICO 🤑":
            category = "ido_ico"
        case "Ambassador Programs 👥":
            category = "ambassador_programs"
        case "NFT 🖼":
            category = "nft"
    await state.update_data(category=category)
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
        date = message.text.split(".")
        try:
            if int(date[0]) <= 31 and int(date[1]) <= 12 and int(date[2]) >= 1000:
                await message.answer(phrases["input_start_time"])
                valid_date = f"{date[2]}-{date[1]}-{date[0]}"
                await state.update_data(start_date=valid_date)
                await state.set_state(PostForm.GET_START_TIME)
            else:
                await message.answer(
                    text="Неверный формат даты. Введите дату еще раз в формате дд.мм.гггг UTC"
                )
        except Exception:
            await message.answer(
                text="Неверный формат даты. Введите дату еще раз в формате дд.мм.гггг UTC"
            )


async def get_start_time(message: Message, bot: Bot, state: FSMContext):
    if message.text == "-":
        await message.answer(phrases["input_end_date"])
        await state.set_state(PostForm.GET_END_DATE)
    else:
        time = message.text.split(":")
        try:
            if int(time[0]) <= 23 and int(time[1]) <= 59:
                await message.answer(phrases["input_end_date"])
                await state.update_data(start_time=f"{time[0]}:{time[1]}")
                await state.set_state(PostForm.GET_END_DATE)
            else:
                await message.answer(
                    text="Неверный формат времени. Введите время еще раз в формате чч.мм UTC"
                )
        except Exception:
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
        date = message.text.split(".")
        try:
            if int(date[0]) <= 31 and int(date[1]) <= 12 and int(date[2]) >= 1000:
                await message.answer(phrases["input_end_time"])
                valid_date = f"{date[2]}-{date[1]}-{date[0]}"
                await state.update_data(end_date=valid_date)
                await state.set_state(PostForm.GET_END_TIME)
            else:
                await message.answer(
                    text="Неверный формат даты. Введите дату еще раз в формате дд.мм.гггг UTC"
                )
        except Exception:
            await message.answer(
                text="Неверный формат даты. Введите дату еще раз в формате дд.мм.гггг UTC"
            )


async def get_end_time(message: Message, bot: Bot, state: FSMContext):
    if message.text == "-":
        await message.answer(phrases["input_short_description"])
        await state.set_state(PostForm.GET_SHORT_DESCRIPTION)
    else:
        time = message.text.split(":")
        try:
            if int(time[0]) <= 23 and int(time[1]) <= 59:
                await message.answer(phrases["input_short_description"])
                await state.update_data(end_time=f"{time[0]}:{time[1]}")
                await state.set_state(PostForm.GET_SHORT_DESCRIPTION)
            else:
                await message.answer(
                    text="Неверный формат времени. Введите время еще раз в формате чч.мм UTC"
                )
        except Exception:
            await message.answer(
                text="Неверный формат времени. Введите время еще раз в формате чч.мм UTC"
            )


async def get_short_description(message: Message, bot: Bot, state: FSMContext):
    await message.answer(text=phrases["input_full_description"])
    await state.update_data(short_description=message.text, post_uuid=str(uuid4()))
    await state.set_state(PostForm.GET_FULL_DESCRIPTION)


async def get_full_description(message: Message, bot: Bot, state: FSMContext):
    await message.answer(text=phrases["input_media"], reply_markup=get_media_keyboard())
    await state.update_data(full_description=message.html_text)
    await state.set_state(PostForm.GET_MEDIA_FILES)


async def get_media_files(message: Message, bot: Bot, state: FSMContext):
    context_data = await state.get_data()
    post_uuid = context_data.get("post_uuid")
    photos = context_data.get("photos")
    videos = context_data.get("videos")
    if message.content_type == ContentType.PHOTO:
        file = await bot.get_file(message.photo[-1].file_id)
        photo_title = f"media/posts_media/photos/{post_uuid}_photo_{len(photos.split(';')) - 1}.jpg"
        photos += photo_title + ";"
        await state.update_data(photos=photos)
        await bot.download_file(file.file_path, photo_title)
    elif message.content_type == ContentType.VIDEO:
        file = await bot.get_file(message.video.file_id)
        video_title = f"media/posts_media/videos/{post_uuid}_video_{len(videos.split(';')) - 1}.mp4"
        videos += video_title + ";"
        await state.update_data(videos=videos)
        await bot.download_file(file.file_path, video_title)


async def save_media_and_show_post(call: CallbackQuery, bot: Bot, state: FSMContext):
    await call.answer()

    context_data = await state.get_data()
    sender = PostSender(bot=bot, context_data=context_data)

    text, media = sender.show_post_detail_for_admin()

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
        text=phrases["finish_message"],
        chat_id=call.message.chat.id,
        reply_markup=get_publick_keyboard(),
    )
    await state.set_state(PostForm.SEND_POST_TO_USERS)


async def send_post_to_users(
    call: CallbackQuery,
    bot: Bot,
    state: FSMContext,
    users_id: list,
    scheduler: AsyncIOScheduler,
    session_maker: sessionmaker,
):
    await call.answer()
    context_data = await state.get_data()
    sender = PostSender(bot=bot, context_data=context_data)

    if users_id:
        text, media = sender.send_post_to_users(
            session_maker=session_maker, scheduler=scheduler
        )

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
            await asyncio.gather(*tasks)
            await state.clear()
            await call.message.edit_text(
                text="✅ Пост успешно опубликован!",
                reply_markup=return_to_admin_panel_keyboard(),
            )
        except Exception:
            await call.message.answer(
                text="Не удалось опубликовать пост, попробуйте еще раз!"
            )
    else:
        await call.message.edit_text(
            text="✅ Пост успешно опубликован!",
            reply_markup=return_to_admin_panel_keyboard(),
        )
    await state.clear()


create_post_router.callback_query.register(create_post, F.data == "create_post")
create_post_router.message.register(get_title, PostForm.GET_TITLE)
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
create_post_router.callback_query.register(
    save_media_and_show_post, F.data == "save_media", PostForm.GET_MEDIA_FILES
)

send_post_router.callback_query.register(
    send_post_to_users, F.data == "publick_post", PostForm.SEND_POST_TO_USERS
)
send_post_router.callback_query.middleware.register(SendPostMiddleware(scheduler))
