from users_core.utils.phrases import phrases
from users_core.keyboards.subscriptions_keyboard import get_subscriptions_keyboard

from aiogram import Bot, Router, F
from aiogram.types import CallbackQuery, FSInputFile, InputMediaPhoto


new_subscription_router = Router()


async def buy_subscription(call: CallbackQuery, bot: Bot):
    media = InputMediaPhoto(
        media=FSInputFile("users_core/utils/photos/subscription.png"),
        caption=phrases["subscriptions_text"],
    )
    await call.message.edit_media(
        media=media,
        reply_markup=get_subscriptions_keyboard("new_sub"),
    )


new_subscription_router.callback_query.register(
    buy_subscription, F.data == "buy_a_subscription"
)
