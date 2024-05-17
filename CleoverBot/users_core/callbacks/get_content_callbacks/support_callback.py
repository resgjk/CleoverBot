from users_core.utils.phrases import phrases
from users_core.keyboards.return_to_main_keyboard import get_keyboard

from aiogram import Bot, Router, F
from aiogram.types import CallbackQuery, FSInputFile, InputMediaPhoto


support_router = Router()


async def get_support(call: CallbackQuery, bot: Bot):
    media = InputMediaPhoto(
        media=FSInputFile("users_core/utils/photos/support.png"),
        caption=phrases["support_text"],
    )
    await call.message.edit_media(media=media, reply_markup=get_keyboard())


support_router.callback_query.register(get_support, F.data == "support")
