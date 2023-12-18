from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_admin_route_keyboard() -> InlineKeyboardMarkup:
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.button(
        text="🔵 Администраторы", callback_data="simple_administrators"
    )
    keyboard_builder.button(
        text="🔴 Cупер - администраторы", callback_data="super_administrators"
    )
    keyboard_builder.button(
        text="⬅️ Вернуться в главное меню", callback_data="return_to_admin_pannel"
    )
    keyboard_builder.adjust(1, repeat=True)
    return keyboard_builder.as_markup()
