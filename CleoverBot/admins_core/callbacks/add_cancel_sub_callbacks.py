from admins_core.utils.phrases import phrases
from admins_core.keyboards.payment_info_keyboard import get_payment_info_keyboard

from aiogram import Bot, Router, F
from aiogram.types import CallbackQuery


add_cancel_sub_router = Router()


async def add_sub(call: CallbackQuery, bot: Bot):
    await call.answer()
    await call.message.answer(text=phrases["add_sub_to_user"] + phrases["ps_id"])


async def cancel_sub(call: CallbackQuery, bot: Bot):
    await call.answer()
    await call.message.answer(text=phrases["cancel_sub_to_user"] + phrases["ps_id"])


add_cancel_sub_router.callback_query.register(add_sub, F.data == "give_subscribe")
add_cancel_sub_router.callback_query.register(cancel_sub, F.data == "cancel_subscribe")
