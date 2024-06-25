from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_activities_list_keyboard(activities: dict) -> InlineKeyboardMarkup:
    keyboard_builder = InlineKeyboardBuilder()
    for activity in activities.keys():
        keyboard_builder.button(
            text=activity, callback_data=f"show_activity_events_{activities[activity]}"
        )
    keyboard_builder.button(
        text="⬅️ Return to main menu", callback_data="return_to_main_menu"
    )
    keyboard_builder.adjust(1, repeat=True)
    return keyboard_builder.as_markup()


def get_event_list_keyboard(events: dict, page: str) -> InlineKeyboardMarkup:
    buttons = []
    for event in events.keys():
        buttons.append(
            [
                InlineKeyboardButton(
                    text=event,
                    callback_data=f"show_activity_event_{events[event]}",
                )
            ]
        )

    match page:
        case "first":
            buttons.append(
                [InlineKeyboardButton(text="➡️", callback_data=f"next_events_page")]
            )
        case "middle":
            buttons.append(
                [
                    InlineKeyboardButton(text="⬅️", callback_data=f"back_events_page"),
                    InlineKeyboardButton(text="➡️", callback_data=f"next_events_page"),
                ]
            )
        case "last":
            buttons.append(
                [InlineKeyboardButton(text="⬅️", callback_data=f"back_events_page")]
            )
    buttons.append(
        [InlineKeyboardButton(text="< Back", callback_data="activity_events")]
    )
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def return_to_activity_events_keyboard(activity_id: int) -> InlineKeyboardMarkup:
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.button(
        text="⬅️ Back to events", callback_data=f"show_activity_events_{activity_id}"
    )
    keyboard_builder.adjust(1, repeat=True)
    return keyboard_builder.as_markup()
