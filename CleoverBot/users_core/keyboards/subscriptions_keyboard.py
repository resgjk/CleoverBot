from users_core.config import (
    ONE_MONTH_PRICE,
    THREE_MONTH_PRICE,
    SIX_MONTH_PRICE,
    TWELVE_MONTH_PRICE,
)

from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_subscriptions_keyboard(callbacks_type: str) -> InlineKeyboardMarkup:
    keyboard_builder = InlineKeyboardBuilder()
    if callbacks_type == "new_sub":
        keyboard_builder.button(
            text=f"💸 Month subscription / {ONE_MONTH_PRICE}$",
            callback_data="new_one_month_subscription",
        )
        keyboard_builder.button(
            text=f"💸 Three month subscription / {THREE_MONTH_PRICE}$",
            callback_data="new_three_month_subscription",
        )
        keyboard_builder.button(
            text=f"💸 Six month subscription / {SIX_MONTH_PRICE}$",
            callback_data="new_six_month_subscription",
        )
        keyboard_builder.button(
            text=f"💸 Twelve month subscription / {TWELVE_MONTH_PRICE}$",
            callback_data="new_twelve_month_subscription",
        )
        keyboard_builder.button(
            text="⬅️ Return to main menu", callback_data="return_to_main_menu"
        )
    elif callbacks_type == "renew_sub":
        keyboard_builder.button(
            text=f"💸 Extend for a month / {ONE_MONTH_PRICE}$",
            callback_data="renew_one_month_subscription",
        )
        keyboard_builder.button(
            text=f"💸 Extend for three months / {THREE_MONTH_PRICE}$",
            callback_data="renew_three_month_subscription",
        )
        keyboard_builder.button(
            text=f"💸 Extend for six months / {SIX_MONTH_PRICE}$",
            callback_data="renew_six_month_subscription",
        )
        keyboard_builder.button(
            text=f"💸 Extend for twelve months / {TWELVE_MONTH_PRICE}$",
            callback_data="renew_twelve_month_subscription",
        )
        keyboard_builder.button(text="⬅️ Return to settings", callback_data="settings")
    keyboard_builder.adjust(1, repeat=True)
    return keyboard_builder.as_markup()


def get_buy_subscription_keyboard() -> InlineKeyboardMarkup:
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.button(
        text="💰 Buy a subscription", callback_data="buy_a_subscription"
    )
    return keyboard_builder.as_markup()
