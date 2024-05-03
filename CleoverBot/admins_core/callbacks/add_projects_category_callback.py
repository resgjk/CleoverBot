from admins_core.utils.phrases import phrases
from admins_core.utils.category_form import CategoryForm
from admins_core.utils.category_sender import CategorySender
from admins_core.keyboards.save_new_projects_category_media_keyboard import (
    get_media_keyboard,
)
from admins_core.keyboards.return_to_categories_route_menu import (
    return_to_categories_route_keyboard,
)
from admins_core.keyboards.save_projects_category_keyboard import get_save_keyboard
from admins_core.middlewares.check_middlewares.check_projects_category import (
    CheckProjectsCategoryMiddleware,
)
from admins_core.middlewares.projects_middlewares.save_projects_category_in_db import (
    SaveProjectsCategoryMiddleware,
)

from aiogram import Bot, Router, F
from aiogram.types import CallbackQuery, Message, ContentType
from aiogram.fsm.context import FSMContext
from aiogram.exceptions import TelegramNetworkError


add_projects_category_router = Router()
get_ptojects_category_title_router = Router()
save_projects_category_in_db_router = Router()


async def start_add_category(call: CallbackQuery, bot: Bot, state: FSMContext):
    await call.answer()
    await call.message.answer(text=phrases["get_projects_category_title"])
    await state.set_state(CategoryForm.GET_TITLE)


async def get_category_title(
    message: Message, bot: Bot, state: FSMContext, result: str
):
    if result == "not_in_db":
        await message.answer(text=phrases["get_projects_category_description"])
        await state.update_data(title=message.text, photos="", videos="")
        await state.set_state(CategoryForm.GET_DESCRIPTION)
    elif result == "in_db":
        await message.answer(
            text="Категория с таким названием уже существует",
            reply_markup=return_to_categories_route_keyboard(),
        )
        await state.clear()
    elif result == "invalid":
        await message.answer(text="Неверный формат названия. Введите название еще раз:")


async def get_category_description(message: Message, bot: Bot, state: FSMContext):
    if message.content_type == ContentType.TEXT:
        await message.answer(
            text=phrases["get_projects_category_media"],
            reply_markup=get_media_keyboard(),
        )
        await state.update_data(description=message.html_text)
        await state.set_state(CategoryForm.GET_MEDIA)
    else:
        await message.answer(text="Неверный формат описания. Введите описание еще раз:")


async def get_media_files(message: Message, bot: Bot, state: FSMContext):
    context_data = await state.get_data()
    title = context_data.get("title")
    photos = context_data.get("photos")
    videos = context_data.get("videos")
    if message.content_type == ContentType.PHOTO:
        file = await bot.get_file(message.photo[-1].file_id)
        photo_title = f"media/projects_media/categories/photos/{title}_photo_{len(photos.split(';')) - 1}.jpg"
        photos += photo_title + ";"
        await state.update_data(photos=photos)
        await bot.download_file(file.file_path, photo_title)
    elif message.content_type == ContentType.VIDEO:
        file = await bot.get_file(message.video.file_id)
        video_title = f"media/projects_media/categories/videos/{title}_video_{len(photos.split(';')) - 1}.mp4"
        videos += video_title + ";"
        await state.update_data(videos=videos)
        await bot.download_file(file.file_path, video_title)


async def save_media_and_show_category(
    call: CallbackQuery, bot: Bot, state: FSMContext
):
    await call.answer()

    context_data = await state.get_data()
    sender = CategorySender(context_data=context_data)

    text, media = sender.show_category_detail_for_admin()

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
        text=phrases["finish_category_message"],
        chat_id=call.message.chat.id,
        reply_markup=get_save_keyboard(),
    )
    await state.set_state(CategoryForm.SAVE_IN_DB)


async def save_category_id_db(
    call: CallbackQuery, bot: Bot, state: FSMContext, result: str
):
    if result == "success":
        await call.answer()
        await call.message.edit_text(
            text="✅ Категория успешно сохранена!",
            reply_markup=return_to_categories_route_keyboard(),
        )
    elif result == "fail":
        await call.answer()
        await call.message.answer(
            text="Не удалось сохранить категорию, попробуйте еще раз!",
            reply_markup=return_to_categories_route_keyboard(),
        )
    await state.clear()


add_projects_category_router.callback_query.register(
    start_add_category, F.data == "add_category"
)
get_ptojects_category_title_router.message.register(
    get_category_title, CategoryForm.GET_TITLE
)
get_ptojects_category_title_router.message.middleware.register(
    CheckProjectsCategoryMiddleware()
)
add_projects_category_router.message.register(
    get_category_description, CategoryForm.GET_DESCRIPTION
)
add_projects_category_router.message.register(get_media_files, CategoryForm.GET_MEDIA)
add_projects_category_router.callback_query.register(
    save_media_and_show_category,
    F.data == "save_projects_category_media",
    CategoryForm.GET_MEDIA,
)

save_projects_category_in_db_router.callback_query.register(
    save_category_id_db, F.data == "save_category", CategoryForm.SAVE_IN_DB
)
save_projects_category_in_db_router.callback_query.middleware.register(
    SaveProjectsCategoryMiddleware()
)
