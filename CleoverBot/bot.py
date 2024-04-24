from datetime import datetime, timedelta, timezone
from typing import Any

from users_core.config import (
    BOT_TOKEN,
    postgres_url,
    scheduler,
    WEBHOOK_DOMAIN,
    WEBHOOK_PATH,
    CALLBACK_PATH,
)
from db.models.users import UserModel
from db.models.transactions import TransactionModel
from users_core.utils.phrases import phrases

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
from users_core.callbacks.payment_callbacks.create_invoice_callback import (
    create_invoice_router,
)
from users_core.callbacks.get_content_callbacks.calendar_callbacks import (
    calendar_router,
    show_event_router,
)
from users_core.utils.commands import set_commands


from admins_core.handlers.start_admin_panel_handler import start_admin_panel_router
from admins_core.callbacks.create_post_callbacks import (
    create_post_router,
    send_post_router,
)
from admins_core.callbacks.users_settings import users_settings_router
from admins_core.callbacks.return_to_admin_pannel_callback import (
    return_to_admin_panel_router,
)
from admins_core.callbacks.admins_route_callback import admins_route_router
from admins_core.callbacks.simple_admins_settings_callback import (
    simple_admins_settings_router,
    add_simple_admin_router,
    delete_simple_admin_router,
)
from admins_core.callbacks.super_admins_settings_callback import (
    super_admins_settings_router,
)
from admins_core.callbacks.add_cancel_sub_callbacks import add_cancel_sub_router
from admins_core.callbacks.add_cancel_sub_callbacks import (
    add_cancel_sub_router,
    get_end_date_for_add_sub_router,
    get_id_for_add_sub_router,
    delete_sub_router,
)
from admins_core.callbacks.super_admins_settings_callback import (
    add_super_admin_router,
    delete_super_admin_router,
    super_admins_settings_router,
)
from admins_core.callbacks.projects_settings_callback import projects_settings_router
from admins_core.callbacks.categories_route_callback import categories_route_router
from admins_core.callbacks.projects_route_callback import projects_route_router
from admins_core.callbacks.add_projects_category_callback import (
    add_projects_category_router,
    get_ptojects_category_title_router,
    save_projects_category_in_db_router,
)
from admins_core.callbacks.delete_projects_category_callback import (
    delete_projects_category_router,
    start_delete_projects_category_router,
)
from admins_core.callbacks.add_project_callback import (
    add_project_router,
    choise_category_for_add_project_router,
    save_project_and_save_router,
    get_title_for_add_project_router,
    save_media_and_links_router,
)

import os
import logging
from contextlib import asynccontextmanager

from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from apsched.check_subscribs import check_subscribs

from fastapi import FastAPI, Request

from sqlalchemy import select
from sqlalchemy.engine import ScalarResult
from sqlalchemy.orm import joinedload


def check_posts_media_folder():
    if not os.path.exists("media"):
        os.mkdir("media")

    dirs = [
        "posts_media",
        "posts_media/photos",
        "posts_media/videos",
        "projects_media",
        "projects_media/categories",
        "projects_media/projects",
        "projects_media/categories/photos",
        "projects_media/categories/videos",
        "projects_media/projects/photos",
        "projects_media/projects/videos",
    ]

    for direction in dirs:
        if not os.path.exists("media/" + direction):
            os.mkdir("media/" + direction)


logging.basicConfig(
    level=logging.INFO,
    format="%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s",
)

bot = Bot(BOT_TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher(storage=MemoryStorage())

async_engine = create_async_engine(postgres_url)
session_maker = get_session_maker(async_engine)


@asynccontextmanager
async def lifespan(app: FastAPI):
    webhook_info = await bot.get_webhook_info()
    if webhook_info.url != (WEBHOOK_DOMAIN + WEBHOOK_PATH):
        await set_commands(bot)

        await proceed_models(async_engine)

        check_posts_media_folder()

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
            create_post_router,
            users_settings_router,
            return_to_admin_panel_router,
            admins_route_router,
            simple_admins_settings_router,
            super_admins_settings_router,
            add_cancel_sub_router,
            get_end_date_for_add_sub_router,
            get_id_for_add_sub_router,
            delete_sub_router,
            send_post_router,
            calendar_router,
            add_simple_admin_router,
            delete_simple_admin_router,
            show_event_router,
            add_super_admin_router,
            delete_super_admin_router,
            create_invoice_router,
            projects_settings_router,
            categories_route_router,
            projects_route_router,
            add_projects_category_router,
            get_ptojects_category_title_router,
            save_projects_category_in_db_router,
            delete_projects_category_router,
            start_delete_projects_category_router,
            add_project_router,
            choise_category_for_add_project_router,
            save_project_and_save_router,
            get_title_for_add_project_router,
            save_media_and_links_router,
        )

        scheduler.add_job(
            check_subscribs,
            trigger="cron",
            hour=12,
            start_date=datetime.now(tz=timezone.utc),
            kwargs={"bot": bot, "session_maker": session_maker},
        )
        scheduler.start()

        await bot.set_webhook(url=WEBHOOK_DOMAIN + WEBHOOK_PATH)

    yield
    await bot.delete_webhook()


app = FastAPI(docs_url=None, redoc_url=None, lifespan=lifespan)


@app.post(CALLBACK_PATH)
async def payment_callback(request: Request):
    body = await request.body()
    data = {}
    for el in body.decode().split("&"):
        el = el.split("=")
        data[el[0]] = el[1]
    async with session_maker() as session:
        async with session.begin():
            res: ScalarResult = await session.execute(
                select(TransactionModel)
                .options(joinedload(TransactionModel.user))
                .where(TransactionModel.uuid.contains(data["invoice_id"]))
            )
            current_transaction: TransactionModel = res.scalars().one_or_none()
            current_transaction.is_success = True
            current_user: UserModel = current_transaction.user
            match current_transaction.type:
                case "one_month":
                    days = 31
                case "three_month":
                    days = 92
                case "six_month":
                    days = 183
                case "twelve_month":
                    days = 365
            if current_user.is_subscriber:
                old_date = list(map(int, current_user.subscriber_until.split("-")))
                old_date = datetime(
                    day=old_date[-1],
                    month=old_date[-2],
                    year=old_date[-3],
                    tzinfo=timezone.utc,
                )
                new_date = old_date + timedelta(days=days)
                current_user.subscriber_until = str(new_date.date())
                new_date = new_date.date().ctime().split()
                await bot.send_message(
                    chat_id=current_user.user_id,
                    text=phrases["subscription_date"]
                    + f"<b>{new_date[2]} {new_date[1]} {new_date[-1]}</b>",
                )
            else:
                date = datetime.now(tz=timezone.utc) + timedelta(days=days)
                current_user.subscriber_until = str(date.date())
                current_user.is_subscriber = True
                date = date.date().ctime().split()
                await bot.send_message(
                    chat_id=current_user.user_id,
                    text=phrases["subscription_date"]
                    + f"<b>{date[2]} {date[1]} {date[-1]}</b>",
                )
            await session.commit()


@app.post(WEBHOOK_PATH)
async def bot_webhook(update: dict[str, Any]):
    telegram_update = types.Update(**update)
    await dp.feed_update(bot=bot, update=telegram_update, session_maker=session_maker)
