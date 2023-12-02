from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_start_keyboard(phrases: dict) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=phrases["week_btn_text"],
                    callback_data=phrases["week_btn_text"],
                )
            ],
            [
                InlineKeyboardButton(
                    text=phrases["month_btn_text"],
                    callback_data=phrases["month_btn_text"],
                )
            ],
            [
                InlineKeyboardButton(
                    text=phrases["three_month_btn_text"],
                    callback_data=phrases["three_month_btn_text"],
                )
            ],
            [
                InlineKeyboardButton(
                    text=phrases["year_btn_text"],
                    callback_data=phrases["year_btn_text"],
                )
            ],
        ]
    )
