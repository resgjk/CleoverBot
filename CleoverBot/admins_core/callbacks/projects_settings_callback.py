from admins_core.utils.phrases import phrases
from admins_core.keyboards.projects_settings_keyboard import (
    get_projects_settings_keyboard,
)

from aiogram import Bot, Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext


projects_settings_router = Router()


async def projects_settings_menu(call: CallbackQuery, bot: Bot, state: FSMContext):
    await state.clear()
    await call.message.edit_text(
        text=phrases["projects_settings"], reply_markup=get_projects_settings_keyboard()
    )


projects_settings_router.callback_query.register(
    projects_settings_menu, F.data == "projects_settings"
)
