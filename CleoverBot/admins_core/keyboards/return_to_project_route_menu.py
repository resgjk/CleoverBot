from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def return_to_project_route_menu_keyboard(project_id: int) -> InlineKeyboardMarkup:
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.button(
        text="⬅️ Вернуться", callback_data=f"choise_project_for_view_{str(project_id)}"
    )
    keyboard_builder.adjust(1, repeat=True)
    return keyboard_builder.as_markup()
