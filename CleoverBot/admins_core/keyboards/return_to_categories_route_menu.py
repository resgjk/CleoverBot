from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def return_to_categories_route_keyboard() -> InlineKeyboardMarkup:
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.button(text="⬅️ Вернуться", callback_data="categories_route")
    keyboard_builder.adjust(1, repeat=True)
    return keyboard_builder.as_markup()
