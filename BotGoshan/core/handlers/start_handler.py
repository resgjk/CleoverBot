from typing import Any

from core.utils.phrases import phrases
from core.keyboards.subscriptions import get_subscriptions_keyboard
from core.middlewares.register_check import RegisterCheckMiddleware

from aiogram.types import Message
from aiogram import Bot, Router
from aiogram.filters import Command


start_router = Router()


async def start_handler(message: Message, bot: Bot) -> Any:
    await message.answer(phrases["start_message"])
    await message.answer(
        phrases["message_with_sub_buttons"],
        reply_markup=get_subscriptions_keyboard(),
    )


start_router.message.register(start_handler, Command(commands="start"))
start_router.message.middleware.register(RegisterCheckMiddleware())