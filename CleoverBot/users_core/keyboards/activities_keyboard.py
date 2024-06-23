from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_activities_keyboard(choice_activities: dict) -> InlineKeyboardMarkup:
    keyboard_builder = InlineKeyboardBuilder()
    for activity in choice_activities.keys():
        keyboard_builder.button(
            text=activity, callback_data=f"set_activity_{choice_activities[activity]}"
        )
    keyboard_builder.button(text="⬅️ Return to settings menu", callback_data="settings")
    keyboard_builder.adjust(1, repeat=True)
    return keyboard_builder.as_markup()
