from users_core.utils.phrases import phrases
from users_core.keyboards.notifications_keyboard import get_notifications_keyboard
from users_core.middlewares.set_middlewares.set_notifications import (
    SetNotificationsMiddleware,
)

from aiogram import Bot, Router, F
from aiogram.types import CallbackQuery, FSInputFile, InputMediaPhoto
from aiogram.exceptions import TelegramBadRequest


set_notifications_router = Router()


async def set_notifications(call: CallbackQuery, bot: Bot, choise_notification):
    try:
        media = InputMediaPhoto(
            media=FSInputFile("users_core/utils/photos/notification.png"),
            caption=phrases["notification_text"],
        )
        await call.message.edit_media(
            media=media,
            reply_markup=get_notifications_keyboard(str(choise_notification)),
        )
    except TelegramBadRequest:
        await call.answer()


set_notifications_router.callback_query.register(
    set_notifications, F.data.contains("set_hours_notification")
)
set_notifications_router.callback_query.middleware.register(
    SetNotificationsMiddleware()
)
