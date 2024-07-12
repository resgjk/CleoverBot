from users_core.utils.phrases import phrases
from users_core.keyboards.main_menu import (
    get_main_menu_keyboard_is_sub,
    get_main_menu_keyboard_is_not_sub,
    get_check_channels,
)
from users_core.middlewares.register_check import RegisterCheckMiddleware

from aiogram.types import Message, FSInputFile, CallbackQuery
from aiogram import Bot, Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext


start_router = Router()


async def start_handler(
    message: Message, bot: Bot, is_subscriber: bool, in_channel: bool, state: FSMContext
):
    await state.clear()
    if in_channel == None:
        await message.answer(
            text=phrases["channels_text"], reply_markup=get_check_channels()
        )
    elif not in_channel:
        await message.answer(
            text=phrases["not_in_channel_text"], reply_markup=get_check_channels()
        )
    elif in_channel:
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


async def check_sub_on_channel(
    call: CallbackQuery,
    bot: Bot,
    is_subscriber: bool,
    in_channel: bool,
    state: FSMContext,
):
    await state.clear()
    await call.answer()
    if in_channel == None:
        await call.message.answer(
            text=phrases["channels_text"], reply_markup=get_check_channels()
        )
    elif not in_channel:
        await call.message.answer(
            text=phrases["not_in_channel_text"], reply_markup=get_check_channels()
        )
    elif in_channel:
        if is_subscriber:
            await call.message.answer_photo(
                photo=FSInputFile("users_core/utils/photos/menu.png"),
                caption=phrases["start_message"],
                reply_markup=get_main_menu_keyboard_is_sub(),
            )
        else:
            await call.message.answer_photo(
                photo=FSInputFile("users_core/utils/photos/menu.png"),
                caption=phrases["start_message"],
                reply_markup=get_main_menu_keyboard_is_not_sub(),
            )


start_router.message.register(start_handler, Command(commands=("start", "menu")))
start_router.message.middleware.register(RegisterCheckMiddleware())
start_router.callback_query.register(check_sub_on_channel, F.data == "check_channels")
start_router.callback_query.middleware.register(RegisterCheckMiddleware())
