from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def choice_withdraw_request_keyboard(requests: dict, page: str) -> InlineKeyboardMarkup:
    buttons = []
    for request in requests.keys():
        buttons.append(
            [
                InlineKeyboardButton(
                    text=request,
                    callback_data=f"show_withdraw_request_{requests[request]}",
                )
            ]
        )

    match page:
        case "first":
            buttons.append(
                [InlineKeyboardButton(text="➡️", callback_data=f"next_requests_page")]
            )
        case "middle":
            buttons.append(
                [
                    InlineKeyboardButton(text="⬅️", callback_data=f"back_requests_page"),
                    InlineKeyboardButton(text="➡️", callback_data=f"next_requests_page"),
                ]
            )
        case "last":
            buttons.append(
                [InlineKeyboardButton(text="⬅️", callback_data=f"back_requests_page")]
            )
    buttons.append(
        [
            InlineKeyboardButton(
                text="⬅️ Вернуться", callback_data=f"return_to_admin_pannel"
            )
        ]
    )
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def return_to_requests_keyboard() -> InlineKeyboardMarkup:
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.button(text="⬅️ Назад", callback_data="withdraw_request")
    keyboard_builder.adjust(1, repeat=True)
    return keyboard_builder.as_markup()
