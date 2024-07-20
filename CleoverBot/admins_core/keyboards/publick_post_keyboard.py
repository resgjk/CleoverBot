from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_publick_keyboard() -> InlineKeyboardMarkup:
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.button(
        text="📤 Опубликовать событие", callback_data="publick_post"
    )
    keyboard_builder.button(
        text="⏰ Опубликовать отложенное событие", callback_data="publick_delayed_post"
    )
    keyboard_builder.button(text="✍️ Изменить событие", callback_data="create_post")
    keyboard_builder.adjust(1, repeat=True)
    return keyboard_builder.as_markup()


def get_refactor_keyboard() -> InlineKeyboardMarkup:
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.button(text="✍️ Изменить событие", callback_data="create_post")
    keyboard_builder.adjust(1, repeat=True)
    return keyboard_builder.as_markup()
