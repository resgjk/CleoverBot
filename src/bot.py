from config import BOT_TOKEN
from phrases import ru, en
from keyboards import start_keyboard

import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message


dp = Dispatcher()
phrases = {}


@dp.message(CommandStart())
async def cmd_start_handler(message: Message):
    lg = message.from_user.language_code
    if lg == "ru":
        phrases = ru.phrases
    else:
        phrases = en.phrases

    msg = await message.answer(
        phrases["hello"], reply_markup=start_keyboard.get_start_keyboard(phrases)
    )


async def main():
    bot = Bot(BOT_TOKEN, parse_mode=ParseMode.HTML)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
