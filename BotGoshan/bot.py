from core.config import BOT_TOKEN
from core.keyboards import start_keyboard
from core.phrases import ru, en

import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.types import Message
from aiogram.filters import CommandStart


dp = Dispatcher()


@dp.message(CommandStart())
async def cmd_start_handler(message: Message):
    lg = message.from_user.language_code
    if lg == "ru":
        phrases = ru.phrases
    else:
        phrases = en.phrases

    await message.answer(
        phrases["hello"]
    )
    await message.answer(
        phrases["description"], reply_markup=start_keyboard.get_start_keyboard(phrases)
    )


async def main():
    bot = Bot(BOT_TOKEN, parse_mode=ParseMode.HTML)

    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
