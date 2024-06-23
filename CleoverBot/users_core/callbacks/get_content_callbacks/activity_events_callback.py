from users_core.utils.phrases import phrases
from users_core.keyboards.activities_list_keyboard import get_activities_list_keyboard
from users_core.middlewares.get_middlewares.get_activities_list import (
    GetActivitiesListMiddleware,
)

from aiogram import Bot, Router, F
from aiogram.types import CallbackQuery, FSInputFile, InputMediaPhoto


activity_events_router = Router()


async def show_activities_list(call: CallbackQuery, bot: Bot, activities: dict):
    media = InputMediaPhoto(
        media=FSInputFile("users_core/utils/photos/activities.png"),
        caption=phrases["activities_list"],
    )
    await call.message.edit_media(
        media=media, reply_markup=get_activities_list_keyboard(activities)
    )


activity_events_router.callback_query.register(
    show_activities_list, F.data == "activity_events"
)
activity_events_router.callback_query.middleware.register(GetActivitiesListMiddleware())
