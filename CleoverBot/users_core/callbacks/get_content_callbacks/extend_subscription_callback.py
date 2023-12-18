from datetime import datetime

from users_core.utils.phrases import phrases
from users_core.keyboards.subscriptions_keyboard import get_subscriptions_keyboard
from users_core.middlewares.get_middlewares.get_expiration_date import (
    GetExpirationDateMiddleware,
)

from aiogram import Bot, Router, F
from aiogram.types import CallbackQuery


renew_subscription_router = Router()


async def extend_subscription(call: CallbackQuery, bot: Bot, expiration_date):
    expiration_date = list(map(int, str(expiration_date).split("-")))
    date = (
        datetime(
            year=expiration_date[0], month=expiration_date[1], day=expiration_date[2]
        )
        .date()
        .ctime()
        .split()
    )
    await call.message.edit_text(
        text="🔑 *Subscription*\n\n"
        + " ".join(
            (
                phrases["expiration_sub_date"],
                "<b>" + date[2],
                date[1],
                date[-1] + "</b>",
            )
        )
        + phrases["renew_subscription"],
        reply_markup=get_subscriptions_keyboard("renew_sub"),
    )


renew_subscription_router.callback_query.register(
    extend_subscription, F.data == "subscription"
)
renew_subscription_router.callback_query.middleware.register(
    GetExpirationDateMiddleware()
)
