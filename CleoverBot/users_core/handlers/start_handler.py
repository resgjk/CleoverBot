from users_core.utils.phrases import phrases
from users_core.keyboards.main_menu import (
    get_main_menu_keyboard_is_sub,
    get_main_menu_keyboard_is_not_sub,
)
from users_core.middlewares.register_check import RegisterCheckMiddleware

from aiogram.types import Message, FSInputFile
from aiogram import Bot, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext


start_router = Router()


async def start_handler(
    message: Message, bot: Bot, is_subscriber: bool, state: FSMContext
):
    await state.clear()
    if is_subscriber:
        await message.answer_photo(
            photo=FSInputFile("users_core/utils/photos/menu.png"),
            caption=phrases["start_message"],
            reply_markup=get_main_menu_keyboard_is_sub(),
        )
    else:
        await message.answer_photo(
            photo=FSInputFile("users_core/utils/photos/menu.png"),
            caption=phrases["start_message"],
            reply_markup=get_main_menu_keyboard_is_not_sub(),
        )


start_router.message.register(start_handler, Command(commands=("start", "menu")))
start_router.message.middleware.register(RegisterCheckMiddleware())
