from aiogram.types import InlineKeyboardMarkup
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
