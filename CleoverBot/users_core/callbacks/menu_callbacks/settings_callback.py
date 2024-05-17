from users_core.utils.phrases import phrases
from users_core.keyboards.settings_keyboard import get_settings_keyboard

from aiogram import Bot, Router, F
from aiogram.types import CallbackQuery, FSInputFile, InputMediaPhoto


settings_router = Router()


async def get_settings(call: CallbackQuery, bot: Bot):
    media = InputMediaPhoto(
        media=FSInputFile("users_core/utils/photos/settings.png"),
        caption=phrases["settings_text"],
    )
    await call.message.edit_media(media=media, reply_markup=get_settings_keyboard())


settings_router.callback_query.register(get_settings, F.data == "settings")
