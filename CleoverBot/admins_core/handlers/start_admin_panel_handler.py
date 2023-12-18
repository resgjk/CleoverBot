from typing import Any

from admins_core.utils.phrases import phrases
from admins_core.keyboards.start_keyboard import get_start_keyboard
from admins_core.middlewares.check_middlewares.chekc_admin import CheckAdminMiddleware

from aiogram.types import Message
from aiogram import Bot, Router
from aiogram.filters import Command


start_admin_panel_router = Router()


async def start_admin_panel(
    message: Message, bot: Bot, is_admin: bool, is_super_admin: bool
):
    if is_admin:
        await message.answer(
            phrases["start_message"], reply_markup=get_start_keyboard(is_super_admin)
        )


start_admin_panel_router.message.register(
    start_admin_panel, Command(commands=("admin"))
)
start_admin_panel_router.message.middleware.register(CheckAdminMiddleware())
