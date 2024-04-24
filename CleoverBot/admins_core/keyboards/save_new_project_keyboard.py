from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_save_keyboard() -> InlineKeyboardMarkup:
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.button(text="📤 Сохранить проект", callback_data="save_project")
    keyboard_builder.button(text="✍️ Изменить проект", callback_data="add_project")
    keyboard_builder.adjust(1, repeat=True)
    return keyboard_builder.as_markup()
