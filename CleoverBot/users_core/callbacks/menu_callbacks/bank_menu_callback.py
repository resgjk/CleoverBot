from users_core.utils.phrases import phrases
from users_core.keyboards.bank_settings_keyboard import get_bank_keyboard
from users_core.middlewares.get_middlewares.get_choise_bank import (
    GetChoiseBankMiddleware,
)

from aiogram import Bot, Router, F
from aiogram.types import CallbackQuery


bank_menu_router = Router()


async def bank_menu(call: CallbackQuery, bot: Bot, choise_bank):
    await call.message.edit_text(
        text=phrases["bank_text"],
        reply_markup=get_bank_keyboard(str(choise_bank)),
    )


bank_menu_router.callback_query.register(bank_menu, F.data == "your_bank")
bank_menu_router.callback_query.middleware.register(GetChoiseBankMiddleware())
