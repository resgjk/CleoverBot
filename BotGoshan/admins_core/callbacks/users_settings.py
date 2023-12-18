from admins_core.utils.phrases import phrases
from admins_core.keyboards.users_settings_keyboard import get_users_settings_keyboard

from aiogram import Bot, Router, F
from aiogram.types import CallbackQuery


users_settings_router = Router()


async def users_settings(call: CallbackQuery, bot: Bot):
    await call.message.edit_text(
        text=phrases["users_settings"], reply_markup=get_users_settings_keyboard()
    )


users_settings_router.callback_query.register(
    users_settings, F.data == "users_settings"
)
