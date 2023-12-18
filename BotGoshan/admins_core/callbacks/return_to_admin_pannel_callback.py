from typing import Any

from admins_core.utils.phrases import phrases
from admins_core.keyboards.start_keyboard import get_start_keyboard
from admins_core.middlewares.check_middlewares.chekc_admin import CheckAdminMiddleware

from aiogram.types import CallbackQuery
from aiogram import Bot, Router, F


return_to_admin_panel_router = Router()


async def return_to_admin_panel(
    call: CallbackQuery, bot: Bot, is_admin: bool, is_super_admin: bool
):
    if is_admin:
        await call.message.edit_text(
            phrases["start_message"], reply_markup=get_start_keyboard(is_super_admin)
        )


return_to_admin_panel_router.callback_query.register(
    return_to_admin_panel, F.data == "return_to_admin_pannel"
)
return_to_admin_panel_router.callback_query.middleware.register(CheckAdminMiddleware())
