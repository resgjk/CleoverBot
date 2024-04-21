from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_projects_settings_keyboard() -> InlineKeyboardMarkup:
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.button(text="🗂 Категории", callback_data="categories_route")
    keyboard_builder.button(text="💼 Проекты", callback_data="projects_route")
    keyboard_builder.button(text="⬅️ Назад", callback_data="return_to_admin_pannel")
    keyboard_builder.adjust(1, repeat=True)
    return keyboard_builder.as_markup()
