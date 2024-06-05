from admins_core.utils.phrases import phrases
from admins_core.utils.category_form import CategoryForm
from admins_core.utils.category_sender import CategorySender
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

from uuid import uuid4

from aiogram import Bot, Router, F
from aiogram.types import CallbackQuery, Message, ContentType, FSInputFile
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
        await state.update_data(title=message.text)
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
        await message.answer(text=phrases["get_projects_category_media"])
        await state.update_data(
            description=message.html_text, project_category_uuid=str(uuid4())
        )
        await state.set_state(CategoryForm.GET_MEDIA)
    else:
        await message.answer(text="Неверный формат описания. Введите описание еще раз:")


async def get_media_files(message: Message, bot: Bot, state: FSMContext):
    context_data = await state.get_data()
    project_category_uuid = context_data.get("project_category_uuid")
    if message.content_type == ContentType.PHOTO:
        file = await bot.get_file(message.photo[-1].file_id)
        photo_title = (
            f"media/projects_media/categories/photos/{project_category_uuid}.jpg"
        )
        await state.update_data(media=photo_title, media_type="photo")
        await bot.download_file(file.file_path, photo_title)
        await state.set_state(CategoryForm.SAVE_MEDIA_AND_SHOW_CATEGORY)
    elif message.content_type == ContentType.VIDEO:
        file = await bot.get_file(message.video.file_id)
        video_title = (
            f"media/projects_media/categories/videos/{project_category_uuid}.mp4"
        )
        await state.update_data(media=video_title, media_type="video")
        await bot.download_file(file.file_path, video_title)
        await state.set_state(CategoryForm.SAVE_MEDIA_AND_SHOW_CATEGORY)
    elif message.content_type == ContentType.TEXT and message.text == "-":
        await state.update_data(media=None, media_type=None)
        await state.set_state(CategoryForm.SAVE_MEDIA_AND_SHOW_CATEGORY)

    state_type = await state.get_state()
    if state_type == CategoryForm.SAVE_MEDIA_AND_SHOW_CATEGORY:
        context_data = await state.get_data()
        sender = CategorySender(context_data=context_data)

        text, media = sender.show_category_detail_for_admin()
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
                catgory_photo = FSInputFile("users_core/utils/photos/categories.png")
                await bot.send_photo(
                    chat_id=message.chat.id, photo=catgory_photo, caption=text
                )
        else:
            catgory_photo = FSInputFile("users_core/utils/photos/categories.png")
            await bot.send_photo(
                chat_id=message.chat.id, photo=catgory_photo, caption=text
            )

        await bot.send_message(
            text=phrases["finish_category_message"],
            chat_id=message.chat.id,
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
save_projects_category_in_db_router.callback_query.register(
    save_category_id_db, F.data == "save_category", CategoryForm.SAVE_IN_DB
)
save_projects_category_in_db_router.callback_query.middleware.register(
    SaveProjectsCategoryMiddleware()
)
