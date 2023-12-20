from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def return_to_user_settings_keyboard() -> InlineKeyboardMarkup:
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.button(
        text="⬅️ Вернуться к настройкам пользователей", callback_data="users_settings"
    )
    keyboard_builder.adjust(1, repeat=True)
    return keyboard_builder.as_markup()
