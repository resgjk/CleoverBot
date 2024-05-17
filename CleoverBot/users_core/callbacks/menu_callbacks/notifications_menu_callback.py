from users_core.utils.phrases import phrases
from users_core.keyboards.notifications_keyboard import get_notifications_keyboard
from users_core.middlewares.get_middlewares.get_choise_notification import (
    GetChoiseNotificationMiddleware,
)

from aiogram import Bot, Router, F
from aiogram.types import CallbackQuery, FSInputFile, InputMediaPhoto


notifications_menu_router = Router()


async def notifications_menu(call: CallbackQuery, bot: Bot, choise_notification):
    media = InputMediaPhoto(
        media=FSInputFile("users_core/utils/photos/notification.png"),
        caption=phrases["notification_text"],
    )
    await call.message.edit_media(
        media=media,
        reply_markup=get_notifications_keyboard(str(choise_notification)),
    )


notifications_menu_router.callback_query.register(
    notifications_menu, F.data == "notification"
)
notifications_menu_router.callback_query.middleware.register(
    GetChoiseNotificationMiddleware()
)
