from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_categories_route_keyboard() -> InlineKeyboardMarkup:
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.button(text="➕ Добавить категорию", callback_data="add_category")
    keyboard_builder.button(text="🚫 Удалить категорию", callback_data="delete_category")
    keyboard_builder.button(text="⬅️ Назад", callback_data="projects_settings")
    keyboard_builder.adjust(1, repeat=True)
    return keyboard_builder.as_markup()
