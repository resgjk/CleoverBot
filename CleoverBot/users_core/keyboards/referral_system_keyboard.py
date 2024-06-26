from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_referral_system_keyboard() -> InlineKeyboardMarkup:
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.button(text="💰 Withdraw money", callback_data="withdraw_money")
    keyboard_builder.button(text="⬅️ Return to settings", callback_data="settings")
    keyboard_builder.adjust(1, repeat=True)
    return keyboard_builder.as_markup()
