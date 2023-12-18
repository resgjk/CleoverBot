from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_simple_admins_settings_keyboard() -> InlineKeyboardMarkup:
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.button(
        text="➕ Добавить администратора", callback_data="add_simple_admin"
    )
    keyboard_builder.button(
        text="🚫 Удалить администратора", callback_data="delete_simple_admin"
    )
    keyboard_builder.button(text="⬅️ Назад", callback_data="admins_settings")
    keyboard_builder.adjust(1, repeat=True)
    return keyboard_builder.as_markup()
