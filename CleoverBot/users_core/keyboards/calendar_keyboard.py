from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_calendar_keyboard(events) -> InlineKeyboardMarkup:
    buttons = []
    buttons.append(
        [
            InlineKeyboardButton(text="⬅️", callback_data="back_date"),
            InlineKeyboardButton(text="➡️", callback_data="next_date"),
        ]
    )
    for event in events:
        buttons.append(
            [
                InlineKeyboardButton(
                    text=event[0], callback_data=f"show_event_{event[0]}"
                )
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
