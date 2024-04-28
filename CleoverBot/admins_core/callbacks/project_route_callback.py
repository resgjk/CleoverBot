from admins_core.utils.phrases import phrases
from admins_core.keyboards.return_to_projects_settings import (
    return_to_projects_settings_keyboard,
)
from admins_core.middlewares.projects_middlewares.delete_project_middlewares import (
    DeleteProjectMiddleware,
)

from aiogram import Bot, Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext


delete_project_router = Router()


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


delete_project_router.callback_query.register(
    delete_project, F.data.contains("delete_project_")
)
delete_project_router.callback_query.middleware.register(DeleteProjectMiddleware())
