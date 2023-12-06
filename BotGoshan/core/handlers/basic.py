from typing import Any

from core.utils.phrases import phrases
from core.keyboards.subscriptions import get_subscriptions_keyboard

from aiogram.types import Message
from aiogram import Bot


async def start_handler(message: Message, bot: Bot) -> Any:
    await message.answer(phrases["start_message"])
    await message.answer(
        phrases["message_with_sub_buttons"],
        reply_markup=get_subscriptions_keyboard(),
    )
