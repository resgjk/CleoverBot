from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_infl_type_keyboard() -> InlineKeyboardMarkup:
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.button(text="🔷 INFLUENCER", callback_data="average_infl")
    keyboard_builder.button(
        text="🔶 INFLUENCER FROM AGENCY", callback_data="agency_infl"
    )
    keyboard_builder.adjust(1, repeat=True)
    return keyboard_builder.as_markup()
