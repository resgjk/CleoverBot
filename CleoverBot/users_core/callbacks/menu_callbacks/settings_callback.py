from users_core.utils.phrases import phrases
from users_core.keyboards.settings_keyboard import get_settings_keyboard

from aiogram import Bot, Router, F
from aiogram.types import CallbackQuery


settings_router = Router()


async def get_settings(call: CallbackQuery, bot: Bot):
    await call.message.edit_text(
        text=phrases["settings_text"], reply_markup=get_settings_keyboard()
    )


settings_router.callback_query.register(get_settings, F.data == "settings")
