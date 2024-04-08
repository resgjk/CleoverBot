from users_core.utils.phrases import phrases
from users_core.keyboards.bank_settings_keyboard import get_bank_keyboard
from users_core.middlewares.set_middlewares.set_bank import SetBankMiddleware

from aiogram import Bot, Router, F
from aiogram.types import CallbackQuery
from aiogram.exceptions import TelegramBadRequest


set_bank_router = Router()


async def set_bank(call: CallbackQuery, bot: Bot, choise_bank):
    try:
        await call.message.edit_text(
            text=phrases["bank_text"],
            reply_markup=get_bank_keyboard(choise_bank),
        )
    except TelegramBadRequest:
        await call.answer()


set_bank_router.callback_query.register(set_bank, F.data.contains("set_bank"))
set_bank_router.callback_query.middleware.register(SetBankMiddleware())
