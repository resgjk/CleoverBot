from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_links_keyboard() -> InlineKeyboardMarkup:
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.button(
        text="💾 Сохранить ссылки", callback_data="save_project_links"
    )
    keyboard_builder.adjust(1, repeat=True)
    return keyboard_builder.as_markup()
