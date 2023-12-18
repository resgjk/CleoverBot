from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def return_to_admin_panel_keyboard() -> InlineKeyboardMarkup:
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.button(
        text="⬅️ Вернуться в главное меню", callback_data="return_to_admin_pannel"
    )
    keyboard_builder.adjust(1, repeat=True)
    return keyboard_builder.as_markup()
