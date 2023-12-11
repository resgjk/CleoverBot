from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_settings_keyboard() -> InlineKeyboardMarkup:
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.button(text="🔑 Subscription", callback_data="subscription")
    keyboard_builder.button(text="🔔 Notification", callback_data="notification")
    keyboard_builder.button(text="💸 Your bank", callback_data="your_bank")
    keyboard_builder.button(
        text="< Return to main menu", callback_data="return_to_main_menu"
    )
    keyboard_builder.adjust(1, repeat=True)
    return keyboard_builder.as_markup()
