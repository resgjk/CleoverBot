from users_core.utils.phrases import phrases
from users_core.keyboards.activities_keyboard import get_activities_keyboard
from users_core.middlewares.get_middlewares.get_choise_activities import (
    GetChoiseActivitiesMiddleware,
)

from aiogram import Bot, Router, F
from aiogram.types import CallbackQuery, FSInputFile, InputMediaPhoto


activities_menu_router = Router()


async def activities_menu(call: CallbackQuery, bot: Bot, choice_activities: dict):
    media = InputMediaPhoto(
        media=FSInputFile("users_core/utils/photos/activities.png"),
        caption=phrases["activities_text"],
    )
    await call.message.edit_media(
        media=media,
        reply_markup=get_activities_keyboard(choice_activities),
    )


activities_menu_router.callback_query.register(activities_menu, F.data == "activities")
activities_menu_router.callback_query.middleware.register(
    GetChoiseActivitiesMiddleware()
)
