from admins_core.utils.phrases import phrases
from admins_core.keyboards.admins_route_keyboard import get_admin_route_keyboard

from aiogram import Bot, Router, F
from aiogram.types import CallbackQuery


admins_route_router = Router()


async def admins_route(call: CallbackQuery, bot: Bot):
    await call.message.edit_text(
        text=phrases["admins_route"], reply_markup=get_admin_route_keyboard()
    )


admins_route_router.callback_query.register(admins_route, F.data == "admins_settings")
