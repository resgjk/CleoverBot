from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_accept_request_keyboard(request_uuid: str) -> InlineKeyboardMarkup:
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.button(
        text="✅ Заявка выполнена", callback_data=f"accept_request_{request_uuid}"
    )
    keyboard_builder.adjust(1, repeat=True)
    return keyboard_builder.as_markup()


def get_accept_request_keyboard_with_back(request_uuid: str) -> InlineKeyboardMarkup:
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.button(
        text="✅ Заявка выполнена",
        callback_data=f"accept_request_with_back_{request_uuid}",
    )
    keyboard_builder.button(text="⬅️ Назад", callback_data="withdraw_request")
    keyboard_builder.adjust(1, repeat=True)
    return keyboard_builder.as_markup()
