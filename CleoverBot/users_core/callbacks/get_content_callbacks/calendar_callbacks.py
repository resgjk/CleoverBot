from users_core.keyboards.calendar_keyboard import (
    get_calendar_keyboard,
    return_to_calendar_keyboard,
)
from users_core.middlewares.get_middlewares.calendar import (
    CalendarMiddleware,
    GetEventDetails,
)
from users_core.utils.calendar_event_sender import CalendarEventSender

import logging

from aiogram import Bot, Router, F
from aiogram.types import CallbackQuery, FSInputFile, InputMediaPhoto
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
    date = ".".join(str(context_data.get("curr_date")).split("-")[::-1])
    text_header = f"🗓️ {date}\n<b>Qurrent events ✍</b>\n\n"
    text = []
    for event in events_news:
        text.append(f"🔹 <b>{event[0]}</b>\n\t\t•   {event[1]}")
    caption = text_header + f"\n{'-' * 50}\n".join(text)

    if "return_to_calendar" in call.data:
        chat_id = call.message.chat.id

        message_ids_for_delete = []
        for message_number in range(int(call.data.split("_")[-1])):
            message_ids_for_delete.append(call.message.message_id - message_number)

        try:
            await bot.delete_messages(
                chat_id=chat_id, message_ids=message_ids_for_delete
            )
        except Exception as e:
            logging.error(e)
        await bot.send_photo(
            chat_id=call.from_user.id,
            photo=calendar_photo,
            caption=caption,
            reply_markup=get_calendar_keyboard(events_news),
        )
    else:
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
    await bot.delete_message(
        chat_id=call.from_user.id, message_id=call.message.message_id
    )

    sender = CalendarEventSender(event_datails)
    text, media = sender.send_event()

    if media:
        try:
            await bot.send_media_group(
                chat_id=call.message.chat.id,
                media=media,
            )
        except TelegramNetworkError as e:
            logging.error(e)
        await bot.send_message(
            chat_id=call.message.chat.id,
            text=text,
            reply_markup=return_to_calendar_keyboard(len(media)),
        )
    else:
        event_photo = FSInputFile("users_core/utils/photos/event.png")
        await bot.send_photo(
            chat_id=call.message.chat.id,
            photo=event_photo,
            caption=text,
            reply_markup=return_to_calendar_keyboard(0),
        )


calendar_router.callback_query.register(get_calendar, F.data == "calendar")
calendar_router.callback_query.register(
    get_calendar, F.data.contains("return_to_calendar")
)
calendar_router.callback_query.register(get_calendar, F.data == "back_date")
calendar_router.callback_query.register(get_calendar, F.data == "next_date")
calendar_router.callback_query.middleware.register(CalendarMiddleware())

show_event_router.callback_query.register(show_event, F.data.contains("show_event"))
show_event_router.callback_query.middleware.register(GetEventDetails())
