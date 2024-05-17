from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def choise_category_keyboard(
    categories: dict, page: str, type: str
) -> InlineKeyboardMarkup:
    buttons = []
    for category in categories.keys():
        buttons.append(
            [
                InlineKeyboardButton(
                    text=category,
                    callback_data=f"set_project_category_{type}_{categories[category]}",
                )
            ]
        )

    match page:
        case "first":
            buttons.append(
                [
                    InlineKeyboardButton(
                        text="➡️", callback_data=f"next_categories_page_{type}"
                    )
                ]
            )
        case "middle":
            buttons.append(
                [
                    InlineKeyboardButton(
                        text="⬅️", callback_data=f"back_categories_page_{type}"
                    ),
                    InlineKeyboardButton(
                        text="➡️", callback_data=f"next_categories_page_{type}"
                    ),
                ]
            )
        case "last":
            buttons.append(
                [
                    InlineKeyboardButton(
                        text="⬅️", callback_data=f"back_categories_page_{type}"
                    )
                ]
            )
    buttons.append(
        [InlineKeyboardButton(text="< Back", callback_data=f"return_to_main_menu")]
    )
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def get_back_from_categories_keyboard() -> InlineKeyboardMarkup:
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.button(text="< Back", callback_data="return_to_main_menu")
    keyboard_builder.adjust(1, repeat=True)
    return keyboard_builder.as_markup()
