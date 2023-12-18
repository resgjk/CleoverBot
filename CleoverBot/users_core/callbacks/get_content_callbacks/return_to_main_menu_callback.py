from users_core.utils.phrases import phrases
from users_core.keyboards.main_menu import (
    get_main_menu_keyboard_is_not_sub,
    get_main_menu_keyboard_is_sub,
)
from users_core.middlewares.register_check import RegisterCheckMiddleware

from aiogram import Bot, Router, F
from aiogram.types import CallbackQuery


main_menu_router = Router()


async def return_to_main_menu(call: CallbackQuery, bot: Bot, is_subscriber: bool):
    if is_subscriber:
        await call.message.edit_text(
            text=phrases["start_message"], reply_markup=get_main_menu_keyboard_is_sub()
        )
    else:
        await call.message.edit_text(
            text=phrases["start_message_user_isnt_sub"],
            reply_markup=get_main_menu_keyboard_is_not_sub(),
        )


main_menu_router.callback_query.register(
    return_to_main_menu, F.data == "return_to_main_menu"
)
main_menu_router.callback_query.middleware.register(RegisterCheckMiddleware())
