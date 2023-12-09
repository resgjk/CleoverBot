from core.config import BOT_TOKEN, postgres_url

from db.base import Base
from db.engine import create_async_engine, get_session_maker, proceed_models
from core.handlers.start_handler import start_router
from core.callbacks.feedback_callback import feedback_router
from core.callbacks.return_to_main_menu_callback import main_menu_router
from core.callbacks.settings_callback import settings_router
from core.callbacks.activities_callback import activities_router

import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode


async def main():
    logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)

    bot = Bot(BOT_TOKEN, parse_mode=ParseMode.HTML)
    dp = Dispatcher()

    dp.include_routers(
        start_router,
        feedback_router,
        main_menu_router,
        settings_router,
        activities_router,
    )

    async_engine = create_async_engine(postgres_url)
    session_maker = get_session_maker(async_engine)
    await proceed_models(async_engine, Base.metadata)

    await dp.start_polling(bot, session_maker=session_maker)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print("Bot stopped")
