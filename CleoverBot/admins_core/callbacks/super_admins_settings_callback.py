from admins_core.utils.phrases import phrases
from admins_core.keyboards.super_admins_settings_keyboard import (
    get_super_admins_settings_keyboard,
)
from aiogram import Bot, Router, F
from aiogram.types import CallbackQuery


super_admins_settings_router = Router()


async def super_admins_settings(call: CallbackQuery, bot: Bot):
    await call.message.edit_text(
        text=phrases["simple_admins_settings"],
        reply_markup=get_super_admins_settings_keyboard(),
    )


super_admins_settings_router.callback_query.register(
    super_admins_settings, F.data == "super_administrators"
)
