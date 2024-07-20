from users_core.utils.phrases import phrases
from users_core.utils.activity_event_sender import ActivitySender
from users_core.utils.calendar_event_sender import CalendarEventSender
from users_core.keyboards.activities_list_keyboard import (
    get_activities_list_keyboard,
    get_event_list_keyboard,
    return_to_activity_events_keyboard,
)
from users_core.middlewares.get_middlewares.get_activities_list import (
    GetActivitiesListMiddleware,
    GetCurrentActivityEventsMiddleware,
    GetActivityEventDetails,
)

from aiogram import Bot, Router, F
from aiogram.types import CallbackQuery, FSInputFile, InputMediaPhoto, InputMediaVideo
from aiogram.fsm.context import FSMContext
from aiogram.exceptions import TelegramNetworkError


activity_events_list_router = Router()
current_activity_events_router = Router()
activity_event_details_router = Router()


async def show_activities_list(
    call: CallbackQuery, bot: Bot, state: FSMContext, activities: dict
):
    await state.clear()
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


async def show_event_details(
    call: CallbackQuery, bot: Bot, event_details: dict, state: FSMContext
):
    await call.answer()

    sender = CalendarEventSender(event_details)
    text, media = sender.send_event()
    media_type = event_details["media_type"]

    if media:
        try:
            if media_type == "photo":
                message_media = InputMediaPhoto(media=media, caption=text)
                await call.message.edit_media(
                    media=message_media,
                    reply_markup=return_to_activity_events_keyboard(
                        event_details["activity_id"]
                    ),
                )
            elif media_type == "video":
                message_media = InputMediaVideo(media=media, caption=text)
                await call.message.edit_media(
                    media=message_media,
                    reply_markup=return_to_activity_events_keyboard(
                        event_details["activity_id"]
                    ),
                )
        except TelegramNetworkError:
            event_photo = FSInputFile("users_core/utils/photos/event.png")
            event_media = InputMediaPhoto(media=event_photo, caption=text)
            await call.message.edit_media(
                media=event_media,
                reply_markup=return_to_activity_events_keyboard(
                    event_details["activity_id"]
                ),
            )
    else:
        event_photo = FSInputFile("users_core/utils/photos/event.png")
        event_media = InputMediaPhoto(media=event_photo, caption=text)
        await call.message.edit_media(
            media=event_media,
            reply_markup=return_to_activity_events_keyboard(
                event_details["activity_id"]
            ),
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
activity_event_details_router.callback_query.register(
    show_event_details, F.data.contains("show_activity_event")
)
activity_event_details_router.callback_query.middleware.register(
    GetActivityEventDetails()
)
