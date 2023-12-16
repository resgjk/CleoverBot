from users_core.config import BOT_TOKEN, postgres_url

from db.base import Base
from db.engine import create_async_engine, get_session_maker, proceed_models
from users_core.handlers.start_handler import start_router
from users_core.callbacks.get_content_callbacks.feedback_callback import feedback_router
from users_core.callbacks.get_content_callbacks.return_to_main_menu_callback import (
    main_menu_router,
)
from users_core.callbacks.menu_callbacks.settings_callback import settings_router
from users_core.callbacks.get_content_callbacks.buy_subscription_callback import (
    new_subscription_router,
)
from users_core.callbacks.get_content_callbacks.extend_subscription_callback import (
    renew_subscription_router,
)
from users_core.callbacks.get_content_callbacks.support_callback import support_router
from users_core.callbacks.get_content_callbacks.instruction_callback import (
    instruction_router,
)
from users_core.callbacks.menu_callbacks.notifications_menu_callback import (
    notifications_menu_router,
)
from users_core.callbacks.menu_callbacks.bank_menu_callback import bank_menu_router
from users_core.callbacks.menu_callbacks.activities_menu_callback import (
    activities_menu_router,
)
from users_core.callbacks.set_content_callbacks.set_notificatioin_callback import (
    set_notifications_router,
)
from users_core.callbacks.set_content_callbacks.set_bank_callback import set_bank_router
from users_core.callbacks.set_content_callbacks.set_activity_callback import (
    set_activity_router,
)
from users_core.utils.commands import set_commands

from admins_core.handlers.start_admin_panel_handler import start_admin_panel_router

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
        start_admin_panel_router,
    )
    await set_commands(bot)

    async_engine = create_async_engine(postgres_url)
    session_maker = get_session_maker(async_engine)
    await proceed_models(async_engine, Base.metadata)

    await dp.start_polling(bot, session_maker=session_maker)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print("Bot stopped")
