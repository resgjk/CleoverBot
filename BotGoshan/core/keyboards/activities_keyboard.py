from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def get_activities_keyboard() -> ReplyKeyboardMarkup:
    keyboard_builder = ReplyKeyboardBuilder()
    keyboard_builder.button(text="1 Activity", callback_data="1_activity")
    keyboard_builder.button(text="2 Activity", callback_data="2_activity")
    keyboard_builder.button(text="3 Activity", callback_data="3_activity")
    keyboard_builder.button(text="4 Activity", callback_data="4_activity")
    keyboard_builder.button(text="5 Activity", callback_data="5_activity")
    keyboard_builder.button(text="6 Activity", callback_data="6_activity")
    keyboard_builder.button(
        text="⬅️ Return to main menu", callback_data="return_to_main_menu"
    )
    keyboard_builder.adjust(1, repeat=True)
    return keyboard_builder.as_markup(resize_keyboard=True, one_time_keyboard=True)
