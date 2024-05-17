from users_core.utils.phrases import phrases
from users_core.keyboards.bank_settings_keyboard import get_bank_keyboard
from users_core.middlewares.get_middlewares.get_choise_bank import (
    GetChoiseBankMiddleware,
)

from aiogram import Bot, Router, F
from aiogram.types import CallbackQuery, FSInputFile, InputMediaPhoto


bank_menu_router = Router()


async def bank_menu(call: CallbackQuery, bot: Bot, choise_bank):
    media = InputMediaPhoto(
        media=FSInputFile("users_core/utils/photos/bank.png"),
        caption=phrases["bank_text"],
    )
    await call.message.edit_media(
        media=media,
        reply_markup=get_bank_keyboard(str(choise_bank)),
    )


bank_menu_router.callback_query.register(bank_menu, F.data == "your_bank")
bank_menu_router.callback_query.middleware.register(GetChoiseBankMiddleware())
