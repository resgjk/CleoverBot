import logging

from admins_core.utils.phrases import phrases
from admins_core.utils.project_form import ProjectForm
from admins_core.utils.project_sender import ProjectSender
from admins_core.keyboards.choise_project_category_keyboard import (
    choise_category_keyboard,
)
from admins_core.keyboards.return_to_projects_route_menu import (
    return_to_projects_route_keyboard,
)
from admins_core.keyboards.save_new_project_links_keyboard import get_links_keyboard
from admins_core.keyboards.save_new_project_keyboard import get_save_keyboard
from admins_core.middlewares.projects_middlewares.get_categories import (
    CategoriesPagesMiddleware,
)
from admins_core.middlewares.projects_middlewares.choise_category import (
    ChoiseCategoryMiddleware,
)
from admins_core.middlewares.check_middlewares.check_project import (
    CheckProjectMiddleware,
)
from admins_core.middlewares.projects_middlewares.get_id_for_send_project import (
    SendProjectMiddleware,
)

import asyncio
from uuid import uuid4

from aiogram import Bot, Router, F
from aiogram.types import CallbackQuery, Message, ContentType, FSInputFile
from aiogram.fsm.context import FSMContext
from aiogram.exceptions import TelegramNetworkError


type = "for_add_project"
add_project_router = Router()
choise_category_for_add_project_router = Router()
get_title_for_add_project_router = Router()
save_project_and_save_router = Router()
save_media_and_links_router = Router()


async def start_add_project(
    call: CallbackQuery,
    bot: Bot,
    state: FSMContext,
    categories: dict,
    page: str,
    is_full: bool,
):
    await call.answer()
    if call.data == "add_project":
        await call.message.answer(
            text=phrases["choise_project_category"],
            reply_markup=choise_category_keyboard(
                categories=categories, page=page, type=type
            ),
        )
        await state.set_state(ProjectForm.CHOISE_CATEGORY)
    else:
        if is_full:
            await call.message.edit_text(
                text=phrases["choise_project_category"],
                reply_markup=choise_category_keyboard(
                    categories=categories, page=page, type=type
                ),
            )


async def choise_category(
    call: CallbackQuery,
    bot: Bot,
    state: FSMContext,
    choisen_category: dict,
    error=False,
):
    await call.answer()
    if error:
        await call.message.answer(
            text="Не удалось выбрать категорию, попробуйте еще раз!"
        )
    else:
        await call.message.edit_text(
            text=f"Выбрана категория: <b>{choisen_category['title']}</b>"
        )
        await call.message.answer(text=phrases["get_project_title"])
        await state.update_data(
            category_id=choisen_category["id"], category_title=choisen_category["title"]
        )
        await state.set_state(ProjectForm.GET_TITLE)


async def get_project_title(message: Message, bot: Bot, state: FSMContext, result: str):
    if result == "not_in_db":
        await message.answer(text=phrases["get_project_description"])
        await state.update_data(title=message.text)
        await state.set_state(ProjectForm.GET_DESCRIPTION)
    elif result == "in_db":
        await message.answer(
            text="Проект с таким названием уже существует",
            reply_markup=return_to_projects_route_keyboard(),
        )
        await state.clear()
    elif result == "invalid":
        await message.answer(text="Неверный формат названия. Введите название еще раз:")


async def get_project_description(message: Message, bot: Bot, state: FSMContext):
    if message.content_type == ContentType.TEXT:
        await message.answer(
            text=phrases["get_project_links"],
            reply_markup=get_links_keyboard(),
        )
        await state.update_data(
            description=message.html_text, links="", project_uuid=str(uuid4())
        )
        await state.set_state(ProjectForm.GET_LINKS)
    else:
        await message.answer(text="Неверный формат описания. Введите описание еще раз:")


async def get_project_links(message: Message, bot: Bot, state: FSMContext):
    context_data = await state.get_data()
    links = context_data.get("links")
    if message.content_type == ContentType.TEXT:
        links += message.html_text + ";"
        await state.update_data(links=links)


async def start_get_media(
    call: CallbackQuery,
    bot: Bot,
    state: FSMContext,
):
    await call.answer()
    await call.message.answer(
        text=phrases["get_project_media"],
    )
    await state.set_state(ProjectForm.GET_MEDIA)


async def get_media_files(message: Message, bot: Bot, state: FSMContext):
    context_data = await state.get_data()
    project_uuid = context_data.get("project_uuid")
    if message.content_type == ContentType.PHOTO:
        file = await bot.get_file(message.photo[-1].file_id)
        photo_title = f"media/projects_media/projects/photos/{project_uuid}.jpg"
        await state.update_data(media=photo_title, media_type="photo")
        await bot.download_file(file.file_path, photo_title)
        await state.set_state(ProjectForm.SAVE_MEDIA_AND_SHOW_PROJECT)
    elif message.content_type == ContentType.VIDEO:
        file = await bot.get_file(message.video.file_id)
        video_title = f"media/projects_media/projects/videos/{project_uuid}.mp4"
        await state.update_data(media=video_title, media_type="video")
        await bot.download_file(file.file_path, video_title)
        await state.set_state(ProjectForm.SAVE_MEDIA_AND_SHOW_PROJECT)
    elif message.content_type == ContentType.TEXT and message.text == "-":
        await state.update_data(media=None, media_type=None)
        await state.set_state(ProjectForm.SAVE_MEDIA_AND_SHOW_PROJECT)

    state_type = await state.get_state()
    if state_type == ProjectForm.SAVE_MEDIA_AND_SHOW_PROJECT:
        context_data = await state.get_data()
        sender = ProjectSender(context_data=context_data)

        text, media = sender.show_project_detail_for_admin()
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
                await message.answer(text=text)
        else:
            event_photo = FSInputFile("users_core/utils/photos/project.png")
            await bot.send_photo(
                chat_id=message.chat.id, photo=event_photo, caption=text
            )

        await bot.send_message(
            text=phrases["finish_project_message"],
            chat_id=message.chat.id,
            reply_markup=get_save_keyboard(),
        )
        await state.set_state(ProjectForm.SAVE_AND_SEND_NOTIF)


async def send_project_to_users(
    call: CallbackQuery, bot: Bot, state: FSMContext, users_id: list, result: str
):
    await call.answer()
    context_data = await state.get_data()
    sender = ProjectSender(context_data=context_data)

    if result == "success":
        if users_id:
            text, media = sender.send_project()
            media_type = context_data.get("media_type")

            tasks = []
            try:
                for id in users_id:
                    if media:
                        try:
                            if media_type == "photo":
                                task = bot.send_photo(
                                    chat_id=id, photo=media, caption=text
                                )
                            elif media_type == "video":
                                task = bot.send_video(
                                    chat_id=id, video=media, caption=text
                                )
                        except TelegramNetworkError:
                            event_photo = FSInputFile(
                                "users_core/utils/photos/project.png"
                            )
                            task = bot.send_photo(
                                chat_id=id, photo=event_photo, caption=text
                            )
                    else:
                        event_photo = FSInputFile("users_core/utils/photos/project.png")
                        task = bot.send_photo(
                            chat_id=id, photo=event_photo, caption=text
                        )
                tasks.append(task)
                await asyncio.gather(*tasks, return_exceptions=True)
                await call.message.edit_text(
                    text="✅ Проект успешно опубликован!",
                    reply_markup=return_to_projects_route_keyboard(),
                )
            except Exception as e:
                logging.error(e)
                await call.message.answer(
                    text=f"Не удалось опубликовать проект, попробуйте еще раз!\nОшибка: {str(e)}",
                    reply_markup=return_to_projects_route_keyboard(),
                )
        else:
            await call.message.edit_text(
                text="✅ Проект успешно опубликован!",
                reply_markup=return_to_projects_route_keyboard(),
            )
    else:
        await call.message.answer(
            text="Не удалось опубликовать проект, попробуйте еще раз!",
            reply_markup=return_to_projects_route_keyboard(),
        )

    await state.clear()


add_project_router.callback_query.register(start_add_project, F.data == "add_project")
add_project_router.callback_query.register(
    start_add_project, F.data == f"next_categories_page_{type}"
)
add_project_router.callback_query.register(
    start_add_project, F.data == f"back_categories_page_{type}"
)
add_project_router.callback_query.middleware.register(CategoriesPagesMiddleware())
add_project_router.message.register(
    get_project_description, ProjectForm.GET_DESCRIPTION
)
save_media_and_links_router.message.register(get_project_links, ProjectForm.GET_LINKS)
save_media_and_links_router.callback_query.register(
    start_get_media, F.data == "save_project_links", ProjectForm.GET_LINKS
)
save_media_and_links_router.message.register(get_media_files, ProjectForm.GET_MEDIA)
choise_category_for_add_project_router.callback_query.register(
    choise_category,
    F.data.contains(f"set_project_category_{type}_"),
    ProjectForm.CHOISE_CATEGORY,
)
choise_category_for_add_project_router.callback_query.middleware.register(
    ChoiseCategoryMiddleware()
)
get_title_for_add_project_router.message.register(
    get_project_title, ProjectForm.GET_TITLE
)
get_title_for_add_project_router.message.middleware.register(CheckProjectMiddleware())
save_project_and_save_router.callback_query.register(
    send_project_to_users,
    F.data == "save_project",
    ProjectForm.SAVE_AND_SEND_NOTIF,
)
save_project_and_save_router.callback_query.middleware.register(SendProjectMiddleware())
