from users_core.utils.phrases import phrases
from users_core.keyboards.activities_keyboard import get_activities_keyboard
from users_core.middlewares.get_middlewares.get_choise_activities import (
    GetChoiseActivitiesMiddleware,
)

from aiogram import Bot, Router, F
from aiogram.types import CallbackQuery


activities_menu_router = Router()


async def activities_menu(call: CallbackQuery, bot: Bot, choise_activities: dict):
    await call.message.edit_text(
        text=phrases["activities_text"],
        reply_markup=get_activities_keyboard(choise_activities),
    )


activities_menu_router.callback_query.register(activities_menu, F.data == "activities")
activities_menu_router.callback_query.middleware.register(
    GetChoiseActivitiesMiddleware()
)
