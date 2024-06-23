from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def get_activities_keyboard(activities: dict) -> ReplyKeyboardMarkup:
    keyboard_builder = ReplyKeyboardBuilder()
    for activity in activities.keys():
        keyboard_builder.button(text=f"{activities[activity]} | {activity}")
    keyboard_builder.adjust(1, repeat=True)
    return keyboard_builder.as_markup(
        resize_keyboard=True,
        one_time_keyboard=True,
        input_field_placeholder="Выберите категорию:",
    )
