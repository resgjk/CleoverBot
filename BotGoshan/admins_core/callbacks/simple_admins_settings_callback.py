from admins_core.utils.phrases import phrases
from admins_core.keyboards.simple_admins_settings_keyboard import (
    get_simple_admins_settings_keyboard,
)
from aiogram import Bot, Router, F
from aiogram.types import CallbackQuery


simple_admins_settings_router = Router()


async def simple_admins_settings(call: CallbackQuery, bot: Bot):
    await call.message.edit_text(
        text=phrases["simple_admins_settings"],
        reply_markup=get_simple_admins_settings_keyboard(),
    )


simple_admins_settings_router.callback_query.register(
    simple_admins_settings, F.data == "simple_administrators"
)
