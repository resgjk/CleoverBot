from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_media_keyboard() -> InlineKeyboardMarkup:
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.button(text="💾 Сохранить медиа файлы", callback_data="save_media")
    keyboard_builder.adjust(1, repeat=True)
    return keyboard_builder.as_markup()
