from core.phrases import ru, en
from core.keyboards import start_keyboard

from aiogram import Bot
from aiogram.types import Message


async def cmd_start_handler(message: Message, bot: Bot):
    lg = message.from_user.language_code
    if lg == "ru":
        phrases = ru.phrases
    else:
        phrases = en.phrases

    await message.answer(
        phrases["hello"], reply_markup=start_keyboard.get_start_keyboard(phrases)
    )