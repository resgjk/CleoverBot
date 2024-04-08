from admins_core.utils.phrases import phrases
from admins_core.keyboards.payment_info_keyboard import get_payment_info_keyboard

from aiogram import Bot, Router, F
from aiogram.types import CallbackQuery


add_delete_super_admins_router = Router()


async def add_admin(call: CallbackQuery, bot: Bot):
    await call.answer()
    await call.message.answer(text=phrases["add_super_admin"] + phrases["ps_id"])


async def delete_admin(call: CallbackQuery, bot: Bot):
    await call.answer()
    await call.message.answer(text=phrases["delete_super_admin"] + phrases["ps_id"])


add_delete_super_admins_router.callback_query.register(
    add_admin, F.data == "add_super_admin"
)
add_delete_super_admins_router.callback_query.register(
    delete_admin, F.data == "delete_super_admin"
)
