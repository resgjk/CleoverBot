from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_start_keyboard(is_super_admin: bool) -> InlineKeyboardMarkup:
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.button(text="✍️ Создать пост", callback_data="create_post")
    keyboard_builder.button(
        text="🗃 Управление проектами", callback_data="projects_settings"
    )
    keyboard_builder.button(
        text="👥 Настройки пользователей", callback_data="users_settings"
    )
    if is_super_admin:
        keyboard_builder.button(
            text="🤵‍♂️ Управление администраторами", callback_data="admins_settings"
        )
        keyboard_builder.button(
            text="📝 Статистика по агенству", callback_data="agency_statistic"
        )
        keyboard_builder.button(
            text="📤 Заявки на вывод", callback_data="withdraw_request"
        )
    keyboard_builder.adjust(1, repeat=True)
    return keyboard_builder.as_markup()
