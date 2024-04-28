from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_project_route_keyboard(project_id: int) -> InlineKeyboardMarkup:
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.button(
        text="📢 Добавить новость",
        callback_data=f"add_news_for_project_{str(project_id)}",
    )
    keyboard_builder.button(
        text="❌ Удалить проект", callback_data=f"delete_project_{str(project_id)}"
    )
    keyboard_builder.adjust(1, repeat=True)
    return keyboard_builder.as_markup()
