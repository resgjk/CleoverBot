from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_subscriptions_keyboard(callbacks_type: str) -> InlineKeyboardMarkup:
    keyboard_builder = InlineKeyboardBuilder()
    if callbacks_type == "new_sub":
        keyboard_builder.button(
            text="💸 Month subscription / 12$", callback_data="new_month_subscription"
        )
        keyboard_builder.button(
            text="💸 Three month subscription / 30$",
            callback_data="new_three_month_subscription",
        )
        keyboard_builder.button(
            text="💸 Six month subscription / 55$",
            callback_data="new_six_month_subscription",
        )
        keyboard_builder.button(
            text="💸 Twelve month subscription / 90$",
            callback_data="new_twelve_month_subscription",
        )
        keyboard_builder.button(
            text="⬅️ Return to main menu", callback_data="return_to_main_menu"
        )
    elif callbacks_type == "renew_sub":
        keyboard_builder.button(
            text="💸 Extend for a month / 12$", callback_data="renew_month_subscription"
        )
        keyboard_builder.button(
            text="💸 Extend for three months / 30$",
            callback_data="renew_three_month_subscription",
        )
        keyboard_builder.button(
            text="💸 Extend for six months / 55$",
            callback_data="renew_six_month_subscription",
        )
        keyboard_builder.button(
            text="💸 Extend for twelve months / 90$",
            callback_data="renew_twelve_month_subscription",
        )
        keyboard_builder.button(text="⬅️ Return to settings", callback_data="settings")
    keyboard_builder.adjust(1, repeat=True)
    return keyboard_builder.as_markup()
