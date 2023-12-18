from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_payment_info_keyboard() -> InlineKeyboardMarkup:
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.button(text="🗓️ За один месяц", callback_data="one_month_info")
    keyboard_builder.button(text="🗓️ За три месяца", callback_data="three_month_info")
    keyboard_builder.button(text="🗓️ За шесть месяцев", callback_data="six_month_info")
    keyboard_builder.button(text="🗓️ За один год", callback_data="twelve_month_info")
    keyboard_builder.button(text="🗓️ За все время", callback_data="all_month_info")
    keyboard_builder.button(
        text="⬅️ Вернуться в главное меню", callback_data="return_to_admin_pannel"
    )
    keyboard_builder.adjust(1, repeat=True)
    return keyboard_builder.as_markup()
