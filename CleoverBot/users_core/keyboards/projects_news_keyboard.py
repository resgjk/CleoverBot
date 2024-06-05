from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def choise_project_news_keyboard(
    news: dict, page: str, category_id: int
) -> InlineKeyboardMarkup:
    buttons = []
    for one_news in news.keys():
        buttons.append(
            [
                InlineKeyboardButton(
                    text=one_news,
                    callback_data=f"view_project_news_{news[one_news][0]}",
                )
            ]
        )

    match page:
        case "first":
            buttons.append(
                [InlineKeyboardButton(text="➡️", callback_data="next_project_news_page")]
            )
        case "middle":
            buttons.append(
                [
                    InlineKeyboardButton(
                        text="⬅️", callback_data="back_project_news_page"
                    ),
                    InlineKeyboardButton(
                        text="➡️", callback_data="next_project_news_page"
                    ),
                ]
            )
        case "last":
            buttons.append(
                [InlineKeyboardButton(text="⬅️", callback_data="back_project_news_page")]
            )
    buttons.append(
        [
            InlineKeyboardButton(
                text="< Back",
                callback_data=f"set_project_category_for_user_choise_project_{category_id}",
            )
        ]
    )
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def return_to_project_keyboard(project_id: int) -> InlineKeyboardMarkup:
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.button(
        text="< Back", callback_data=f"choise_project_for_user_view_{project_id}"
    )
    keyboard_builder.adjust(1, repeat=True)
    return keyboard_builder.as_markup()
