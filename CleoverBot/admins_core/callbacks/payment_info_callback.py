from admins_core.utils.phrases import phrases
from admins_core.keyboards.payment_info_keyboard import get_payment_info_keyboard

from aiogram import Bot, Router, F
from aiogram.types import CallbackQuery


payment_info_router = Router()


async def payment_info(call: CallbackQuery, bot: Bot):
    await call.message.edit_text(
        text=phrases["payment_info"], reply_markup=get_payment_info_keyboard()
    )


payment_info_router.callback_query.register(payment_info, F.data == "payment_info")
