from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_calendar_keyboard(events) -> InlineKeyboardMarkup:
    buttons = []
    for event in events:
        buttons.append(
            [
                InlineKeyboardButton(
                    text=event[0], callback_data=f"show_event_{event[-1]}"
                )
            ]
        )
    buttons.append(
        [
            InlineKeyboardButton(text="⬅️", callback_data="back_date"),
            InlineKeyboardButton(text="➡️", callback_data="next_date"),
        ]
    )
    buttons.append(
        [
            InlineKeyboardButton(
                text="⬅️ Return to main menu", callback_data="return_to_main_menu"
            )
        ]
    )
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def return_to_calendar_keyboard() -> InlineKeyboardMarkup:
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.button(
        text="⬅️ Return to calendar",
        callback_data="calendar",
    )
    return keyboard_builder.as_markup()
