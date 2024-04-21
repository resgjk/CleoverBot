from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_projects_route_keyboard() -> InlineKeyboardMarkup:
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.button(text="➕ Добавить проект", callback_data="add_project")
    keyboard_builder.button(text="🚫 Удалить проект", callback_data="delete_project")
    keyboard_builder.button(text="⬅️ Назад", callback_data="projects_settings")
    keyboard_builder.adjust(1, repeat=True)
    return keyboard_builder.as_markup()
