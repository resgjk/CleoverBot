from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def return_to_payment_info_keyboard() -> InlineKeyboardMarkup:
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.button(text="⬅️ Назад", callback_data="payment_info")
    keyboard_builder.adjust(1, repeat=True)
    return keyboard_builder.as_markup()
