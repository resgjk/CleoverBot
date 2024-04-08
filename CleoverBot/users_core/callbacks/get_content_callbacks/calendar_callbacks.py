from users_core.keyboards.calendar_keyboard import get_calendar_keyboard
from users_core.middlewares.get_middlewares.calendar import (
    CalendarMiddleware,
    GetEventDetails,
)

from aiogram import Bot, Router, F
from aiogram.types import CallbackQuery, FSInputFile, InputMediaPhoto, InputMediaVideo
from aiogram.fsm.context import FSMContext


calendar_router = Router()
show_event_router = Router()


async def get_calendar(
    call: CallbackQuery, bot: Bot, events_news: list, state: FSMContext
):
    await call.answer()
    context_data = await state.get_data()
    date = ".".join(context_data.get("curr_date").split("-")[::-1])
    text = [f"<b>{date}</b>\nEVENTS:"]
    for event in events_news:
        text.append(f"{event[0]} - {event[1]}")
    text = "\n\n".join(text)
    await call.message.edit_text(
        text=text, reply_markup=get_calendar_keyboard(events_news)
    )


async def show_event(
    call: CallbackQuery, bot: Bot, event_datails: dict, state: FSMContext
):
    await call.answer()
    title = event_datails["title"]
    start_date = event_datails["start_date"]
    start_time = event_datails["start_time"]
    end_date = event_datails["end_date"]
    end_time = event_datails["end_time"]
    full_description = event_datails["full_description"]
    photos = event_datails["photos"]
    if photos:
        photos = event_datails["photos"].split(";")[:-1]
    videos = event_datails["videos"]
    if videos:
        videos = event_datails["videos"].split(";")[:-1]

    text = []
    text.append(f"🗞️ <b>{title}</b>\n\n")
    text.append(f"📜 {full_description}\n\n")
    if start_date:
        date = ".".join(start_date.split("-")[::-1])
        if start_time:
            text.append(f"🗓️ Start date: {date}, {start_time}\n")
        else:
            text.append(f"🗓️ Start date: {date}\n")
    if end_date:
        date = ".".join(end_date.split("-")[::-1])
        if end_time:
            text.append(f"🏁 End date: {date}, {end_time}")
        else:
            text.append(f"🏁 End date: {date}")
    text = "".join(text)

    media = []
    if photos:
        for photo in photos:
            if not media:
                media.append(
                    InputMediaPhoto(
                        type="photo", media=FSInputFile(path=photo), caption=text
                    )
                )
            else:
                media.append(
                    InputMediaPhoto(type="photo", media=FSInputFile(path=photo))
                )
    if videos:
        for video in videos:
            if not media:
                media.append(
                    InputMediaVideo(
                        type="video", media=FSInputFile(path=video), caption=text
                    )
                )
            else:
                media.append(
                    InputMediaVideo(type="video", media=FSInputFile(path=video))
                )
    if media:
        await bot.send_media_group(
            chat_id=call.message.chat.id,
            media=media,
        )
    else:
        await bot.send_message(chat_id=call.message.chat.id, text=text)


calendar_router.callback_query.register(get_calendar, F.data == "calendar")
calendar_router.callback_query.register(get_calendar, F.data == "back_date")
calendar_router.callback_query.register(get_calendar, F.data == "next_date")
calendar_router.callback_query.middleware.register(CalendarMiddleware())

show_event_router.callback_query.register(show_event, F.data.contains("show_event"))
show_event_router.callback_query.middleware.register(GetEventDetails())
