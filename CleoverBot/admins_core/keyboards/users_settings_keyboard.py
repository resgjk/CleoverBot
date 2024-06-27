from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_users_settings_keyboard() -> InlineKeyboardMarkup:
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.button(text="👥 Добавить инфлюенсера", callback_data="add_influencer")
    keyboard_builder.button(text="➕ Выдать подписку", callback_data="give_subscribe")
    keyboard_builder.button(
        text="🚫 Отменить подписку", callback_data="cancel_subscribe"
    )
    keyboard_builder.button(
        text="⬅️ Вернуться в главное меню", callback_data="return_to_admin_pannel"
    )
    keyboard_builder.adjust(1, repeat=True)
    return keyboard_builder.as_markup()
