from core.config import BOT_TOKEN, postgres_url

from db.base import Base
from db.engine import create_async_engine, get_session_maker, proceed_models
from core.handlers.start_handler import start_router
from core.callbacks.feedback_callback import feedback_router
from core.callbacks.return_to_main_menu_callback import main_menu_router
from core.callbacks.settings_callback import settings_router
from core.callbacks.buy_subscription_callback import new_subscription_router
from core.callbacks.extend_subscription_callback import renew_subscription_router
from core.callbacks.support_callback import support_router
from core.callbacks.instruction_callback import instruction_router
from core.callbacks.notifications_menu_callback import notifications_menu_router
from core.callbacks.bank_menu_callback import bank_menu_router
from core.callbacks.activities_menu_callback import activities_menu_router
from core.callbacks.set_notificatioin_callback import set_notifications_router
from core.callbacks.set_bank_callback import set_bank_router
from core.callbacks.set_activity_callback import set_activity_router

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
        new_subscription_router,
        renew_subscription_router,
        support_router,
        instruction_router,
        notifications_menu_router,
        bank_menu_router,
        activities_menu_router,
        set_notifications_router,
        set_bank_router,
        set_activity_router,
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
