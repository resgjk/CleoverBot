from users_core.keyboards.calendar_keyboard import get_calendar_keyboard
from users_core.middlewares.get_middlewares.calendar import (
    CalendarMiddleware,
    GetEventDetails,
)
from users_core.utils.calendar_event_sender import CalendarEventSender

from aiogram import Bot, Router, F
from aiogram.types import CallbackQuery
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

    sender = CalendarEventSender(event_datails)
    text, media = sender.send_event()

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
