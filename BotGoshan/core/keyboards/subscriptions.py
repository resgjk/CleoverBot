from core.utils.phrases import buttons_text

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_subscriptions_keyboard() -> InlineKeyboardMarkup:
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.button(text=buttons_text["week"], callback_data="week")
    keyboard_builder.button(text=buttons_text["month"], callback_data="month")
    keyboard_builder.button(
        text=buttons_text["three_month"], callback_data="three_month"
    )
    keyboard_builder.button(text=buttons_text["year"], callback_data="year")
    keyboard_builder.adjust(1, repeat=True)
    return keyboard_builder.as_markup()
