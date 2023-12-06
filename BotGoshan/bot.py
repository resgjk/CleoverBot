from core.config import BOT_TOKEN, postgres_url
from core.handlers.basic import start_handler
from core.middlewares.register_check import RegisterCheckMiddleware

from db.database import create_async_engine, get_session_maker, proceed_models, BaseModel

import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.filters import Command


async def main():
    logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)

    bot = Bot(BOT_TOKEN, parse_mode=ParseMode.HTML)
    dp = Dispatcher()

    async_engine = create_async_engine(postgres_url)
    session_maker = get_session_maker(async_engine)
    await proceed_models(async_engine, BaseModel.metadata)

    dp.message.middleware.register(RegisterCheckMiddleware())

    dp.message.register(start_handler, Command(commands="start"))

    await dp.start_polling(bot, session_maker=session_maker)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print("Bot stopped")
