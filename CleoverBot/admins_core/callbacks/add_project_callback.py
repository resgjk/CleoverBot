from admins_core.utils.phrases import phrases
from admins_core.utils.project_form import ProjectForm
from admins_core.utils.project_sender import ProjectSender
from admins_core.keyboards.choise_project_category_keyboard import (
    choise_category_keyboard,
)
from admins_core.keyboards.return_to_projects_route_menu import (
    return_to_projects_route_keyboard,
)
from admins_core.keyboards.return_to_admin_panel_keyboard import (
    return_to_admin_panel_keyboard,
)
from admins_core.keyboards.save_new_project_media_keyboard import get_media_keyboard
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

from aiogram import Bot, Router, F
from aiogram.types import CallbackQuery, Message, ContentType
from aiogram.fsm.context import FSMContext


type = "for_add_project"
add_project_router = Router()
choise_category_for_add_project_router = Router()
get_title_for_add_project_router = Router()
save_project_and_save_router = Router()
save_media_and_links_router = Router()


async def start_add_project(
    call: CallbackQuery, bot: Bot, state: FSMContext, categories: dict, page: str
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
        await call.message.answer(
            text=f"Выбрана категория <b>{choisen_category['title']}</b>"
        )
        await call.message.answer(text=phrases["get_project_title"])
        await state.update_data(
            category_id=choisen_category["id"], category_title=choisen_category["title"]
        )
        await state.set_state(ProjectForm.GET_TITLE)


async def get_project_title(message: Message, bot: Bot, state: FSMContext, result: str):
    if result == "not_in_db":
        await message.answer(text=phrases["get_project_description"])
        await state.update_data(title=message.text, photos="", videos="")
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
        await state.update_data(description=message.text, links="")
        await state.set_state(ProjectForm.GET_LINKS)
    else:
        await message.answer(text="Неверный формат описания. Введите описание еще раз:")


async def get_project_links(message: Message, bot: Bot, state: FSMContext):
    context_data = await state.get_data()
    links = context_data.get("links")
    if message.content_type == ContentType.TEXT:
        links += message.text + ";"
        await state.update_data(links=links)


async def start_get_media(
    call: CallbackQuery,
    bot: Bot,
    state: FSMContext,
):
    await call.answer()
    await call.message.answer(
        text=phrases["get_project_media"],
        reply_markup=get_media_keyboard(),
    )
    await state.set_state(ProjectForm.GET_MEDIA)


async def get_media_files(message: Message, bot: Bot, state: FSMContext):
    context_data = await state.get_data()
    title = context_data.get("title")
    photos = context_data.get("photos")
    videos = context_data.get("videos")
    if message.content_type == ContentType.PHOTO:
        file = await bot.get_file(message.photo[-1].file_id)
        photo_title = f"media/projects_media/projects/photos/{title}_photo_{len(photos.split(';')) - 1}.jpg"
        photos += photo_title + ";"
        await state.update_data(photos=photos)
        await bot.download_file(file.file_path, photo_title)
    elif message.content_type == ContentType.VIDEO:
        file = await bot.get_file(message.video.file_id)
        video_title = f"media/projects_media/projects/videos/{title}_video_{len(photos.split(';')) - 1}.mp4"
        videos += video_title + ";"
        await state.update_data(videos=videos)
        await bot.download_file(file.file_path, video_title)


async def save_media_and_show_project(call: CallbackQuery, bot: Bot, state: FSMContext):
    await call.answer()

    context_data = await state.get_data()
    sender = ProjectSender(context_data=context_data)

    text, media = sender.show_project_detail_for_admin()

    if media:
        await bot.send_media_group(
            chat_id=call.message.chat.id,
            media=media,
        )
    else:
        await call.message.answer(text=text)
    await bot.send_message(
        text=phrases["finish_project_message"],
        chat_id=call.message.chat.id,
        reply_markup=get_save_keyboard(),
    )
    await state.set_state(ProjectForm.SAVE_AND_SEND_NOTIF)


async def send_project_to_users(
    call: CallbackQuery,
    bot: Bot,
    state: FSMContext,
    users_id: list,
):
    context_data = await state.get_data()
    sender = ProjectSender(context_data=context_data)

    if users_id:
        text, media = sender.send_project_to_users()

        tasks = []
        try:
            for id in users_id:
                if media:
                    task = bot.send_media_group(
                        chat_id=id,
                        media=media,
                    )
                    tasks.append(task)
                else:
                    task = bot.send_message(chat_id=id, text=text)
                    tasks.append(task)
            await asyncio.gather(*tasks)
            await state.clear()
            await call.answer()
            await call.message.answer(
                text="✅ Проект успешно опубликован!",
                reply_markup=return_to_admin_panel_keyboard(),
            )
        except Exception as e:
            await call.answer()
            await call.message.answer(
                text="Не удалось опубликовать проект, попробуйте еще раз!"
            )
    else:
        await call.answer()
        await call.message.answer(
            text="✅ Проект успешно опубликован!",
            reply_markup=return_to_admin_panel_keyboard(),
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
    start_get_media, F.data == "save_project_links"
)
save_media_and_links_router.message.register(get_media_files, ProjectForm.GET_MEDIA)
save_media_and_links_router.callback_query.register(
    save_media_and_show_project, F.data == "save_project_media"
)

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
