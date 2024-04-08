from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def get_banks_keyboard() -> ReplyKeyboardMarkup:
    keyboard_builder = ReplyKeyboardBuilder()
    keyboard_builder.button(text="Zero bank")
    keyboard_builder.button(text="$100 - 1000")
    keyboard_builder.button(text="$1000 - 10000")
    keyboard_builder.button(text="$10k+")
    keyboard_builder.button(text="Любой бюджет")
    keyboard_builder.adjust(1, repeat=True)
    return keyboard_builder.as_markup(
        one_time_keyboard=True,
        resize_keyboard=True,
        input_field_placeholder="Выберите бюджет:",
    )
