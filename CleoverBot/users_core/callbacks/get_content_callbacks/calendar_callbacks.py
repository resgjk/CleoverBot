from users_core.keyboards.calendar_keyboard import (
    get_calendar_keyboard,
    return_to_calendar_keyboard,
)
from users_core.middlewares.get_middlewares.calendar import (
    CalendarMiddleware,
    GetEventDetails,
)
from users_core.utils.calendar_event_sender import CalendarEventSender

import datetime

from aiogram import Bot, Router, F
from aiogram.types import CallbackQuery, FSInputFile, InputMediaPhoto, InputMediaVideo
from aiogram.fsm.context import FSMContext
from aiogram.exceptions import TelegramNetworkError


calendar_router = Router()
show_event_router = Router()


async def get_calendar(
    call: CallbackQuery, bot: Bot, events_news: list, state: FSMContext
):
    await call.answer()
    context_data = await state.get_data()
    calendar_photo = FSInputFile("users_core/utils/photos/calendar.png")
    date = ".".join(
        str(datetime.date.fromisoformat(context_data.get("curr_date"))).split("-")[::-1]
    )
    text_header = f"🗓️ {date}\n<b>Current events ✍</b>\n\n"
    text = []

    for event in events_news:
        text.append(f"🔹 <b>{event[0]}</b>\n\t\t•   {event[1]}")
    caption = text_header + f"\n{'-' * 50}\n".join(text)

    media = InputMediaPhoto(
        media=calendar_photo,
        caption=caption,
    )
    await call.message.edit_media(
        media=media,
        reply_markup=get_calendar_keyboard(events_news),
    )


async def show_event(
    call: CallbackQuery, bot: Bot, event_datails: dict, state: FSMContext
):
    await call.answer()

    sender = CalendarEventSender(event_datails)
    text, media = sender.send_event()
    media_type = event_datails["media_type"]

    if media:
        try:
            if media_type == "photo":
                message_media = InputMediaPhoto(media=media, caption=text)
                await call.message.edit_media(
                    media=message_media, reply_markup=return_to_calendar_keyboard()
                )
            elif media_type == "video":
                message_media = InputMediaVideo(media=media, caption=text)
                await call.message.edit_media(
                    media=message_media, reply_markup=return_to_calendar_keyboard()
                )
        except TelegramNetworkError:
            event_photo = FSInputFile("users_core/utils/photos/event.png")
            event_media = InputMediaPhoto(media=event_photo, caption=text)
            await call.message.edit_media(
                media=event_media, reply_markup=return_to_calendar_keyboard()
            )
    else:
        event_photo = FSInputFile("users_core/utils/photos/event.png")
        event_media = InputMediaPhoto(media=event_photo, caption=text)
        await call.message.edit_media(
            media=event_media, reply_markup=return_to_calendar_keyboard()
        )


calendar_router.callback_query.register(get_calendar, F.data == "calendar")
calendar_router.callback_query.register(get_calendar, F.data == "back_date")
calendar_router.callback_query.register(get_calendar, F.data == "next_date")
calendar_router.callback_query.middleware.register(CalendarMiddleware())
show_event_router.callback_query.register(show_event, F.data.contains("show_event"))
show_event_router.callback_query.middleware.register(GetEventDetails())
