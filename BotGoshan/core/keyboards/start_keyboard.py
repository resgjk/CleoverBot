from core.config import WEEK_ACCOUNT, MONTH_ACCOUNT, THREE_MONTH_ACCOUNT, YEAR_ACCOUNT

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_start_keyboard(phrases: dict) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=phrases["week_btn_text"],
                    url=WEEK_ACCOUNT,
                )
            ],
            [
                InlineKeyboardButton(
                    text=phrases["month_btn_text"],
                    url=MONTH_ACCOUNT,
                )
            ],
            [
                InlineKeyboardButton(
                    text=phrases["three_month_btn_text"],
                    url=THREE_MONTH_ACCOUNT,
                )
            ],
            [
                InlineKeyboardButton(
                    text=phrases["year_btn_text"],
                    url=YEAR_ACCOUNT,
                )
            ],
        ]
    )
