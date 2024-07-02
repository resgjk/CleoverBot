from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_statistic_type_keyboard() -> InlineKeyboardMarkup:
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.button(
        text="💹 По транзакциям", callback_data="transactions_statistic"
    )
    keyboard_builder.button(text="👥 По инфлюенсерам", callback_data="infl_statistic")
    keyboard_builder.button(text="⬅️ Вернуться", callback_data="return_to_admin_pannel")
    keyboard_builder.adjust(1, repeat=True)
    return keyboard_builder.as_markup()
