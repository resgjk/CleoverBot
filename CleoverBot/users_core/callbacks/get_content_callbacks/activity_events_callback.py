from users_core.utils.phrases import phrases
from users_core.utils.activity_event_sender import ActivitySender
from users_core.keyboards.activities_list_keyboard import (
    get_activities_list_keyboard,
    get_event_list_keyboard,
)
from users_core.middlewares.get_middlewares.get_activities_list import (
    GetActivitiesListMiddleware,
    GetCurrentActivityEventsMiddleware,
)

from aiogram import Bot, Router, F
from aiogram.types import CallbackQuery, FSInputFile, InputMediaPhoto
from aiogram.fsm.context import FSMContext


activity_events_list_router = Router()
current_activity_events_router = Router()


async def show_activities_list(call: CallbackQuery, bot: Bot, activities: dict):
    media = InputMediaPhoto(
        media=FSInputFile("users_core/utils/photos/activities.png"),
        caption=phrases["activities_list"],
    )
    await call.message.edit_media(
        media=media, reply_markup=get_activities_list_keyboard(activities)
    )


async def show_events_list(
    call: CallbackQuery,
    bot: Bot,
    state: FSMContext,
    current_activity: dict,
    current_events: dict,
    is_full: bool,
    page: str,
):
    sender = ActivitySender(current_activity)
    text = sender.send_activity()
    message_media = InputMediaPhoto(
        media=FSInputFile("users_core/utils/photos/activities.png"), caption=text
    )
    await call.message.edit_media(
        media=message_media,
        reply_markup=get_event_list_keyboard(current_events, page),
    )


async def choice_events_page(
    call: CallbackQuery,
    bot: Bot,
    state: FSMContext,
    current_events: dict,
    is_full: bool,
    page: str,
):
    await call.answer()
    if is_full:
        await call.message.edit_reply_markup(
            reply_markup=get_event_list_keyboard(current_events, page),
        )


activity_events_list_router.callback_query.register(
    show_activities_list, F.data == "activity_events"
)
activity_events_list_router.callback_query.middleware.register(
    GetActivitiesListMiddleware()
)
current_activity_events_router.callback_query.register(
    show_events_list, F.data.contains("show_activity_events")
)
current_activity_events_router.callback_query.register(
    choice_events_page, F.data == "next_events_page"
)
current_activity_events_router.callback_query.register(
    choice_events_page, F.data == "back_events_page"
)
current_activity_events_router.callback_query.middleware.register(
    GetCurrentActivityEventsMiddleware()
)
