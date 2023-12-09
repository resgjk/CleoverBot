from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_main_menu_keyboard_is_sub() -> InlineKeyboardMarkup:
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.button(text="Feedback", callback_data="feedback")
    keyboard_builder.button(text="Settings", callback_data="settings")
    keyboard_builder.button(text="Activities", callback_data="activities")
    keyboard_builder.button(text="Instruction", callback_data="instruction")
    keyboard_builder.button(text="Calendar", callback_data="calendar")
    keyboard_builder.button(text="Support", callback_data="support")
    keyboard_builder.adjust(2, repeat=True)
    return keyboard_builder.as_markup()


def get_main_menu_keyboard_is_not_sub() -> InlineKeyboardMarkup:
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.button(text="Feedback", callback_data="feedback")
    keyboard_builder.button(
        text="Buy a subscription", callback_data="buy_a_subscription"
    )
    keyboard_builder.button(text="Support", callback_data="support")
    keyboard_builder.adjust(2, repeat=True)
    return keyboard_builder.as_markup()
