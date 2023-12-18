from users_core.utils.phrases import phrases
from users_core.keyboards.notifications_keyboard import get_notifications_keyboard
from users_core.middlewares.get_middlewares.get_choise_notification import (
    GetChoiseNotificationMiddleware,
)

from aiogram import Bot, Router, F
from aiogram.types import CallbackQuery


notifications_menu_router = Router()


async def notifications_menu(call: CallbackQuery, bot: Bot, choise_notification):
    await call.message.edit_text(
        text=phrases["notification_text"],
        reply_markup=get_notifications_keyboard(str(choise_notification)),
    )


notifications_menu_router.callback_query.register(
    notifications_menu, F.data == "notification"
)
notifications_menu_router.callback_query.middleware.register(
    GetChoiseNotificationMiddleware()
)
