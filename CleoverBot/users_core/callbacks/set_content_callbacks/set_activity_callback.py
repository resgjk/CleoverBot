from users_core.utils.phrases import phrases
from users_core.keyboards.activities_keyboard import get_activities_keyboard
from users_core.middlewares.set_middlewares.set_activities import (
    SetActivitiesMiddleware,
)

from aiogram import Bot, Router, F
from aiogram.types import CallbackQuery, InputMediaPhoto, FSInputFile
from aiogram.exceptions import TelegramBadRequest


set_activity_router = Router()


async def set_activity(call: CallbackQuery, bot: Bot, choise_activities: dict):
    try:
        media = InputMediaPhoto(
            media=FSInputFile("users_core/utils/photos/activities.png"),
            caption=phrases["activities_text"],
        )
        await call.message.edit_media(
            media=media,
            reply_markup=get_activities_keyboard(choise_activities),
        )
    except TelegramBadRequest:
        await call.answer()


set_activity_router.callback_query.register(
    set_activity, F.data.contains("set_activity")
)
set_activity_router.callback_query.middleware.register(SetActivitiesMiddleware())
