from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def choise_project_news_keyboard(
    news: dict, page: str, media_count: int, category_id: int
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
                [
                    InlineKeyboardButton(
                        text="➡️", callback_data=f"next_project_news_page"
                    )
                ]
            )
        case "middle":
            buttons.append(
                [
                    InlineKeyboardButton(
                        text="⬅️", callback_data=f"back_project_news_page"
                    ),
                    InlineKeyboardButton(
                        text="➡️", callback_data=f"next_project_news_page"
                    ),
                ]
            )
        case "last":
            buttons.append(
                [
                    InlineKeyboardButton(
                        text="⬅️", callback_data=f"back_project_news_page"
                    )
                ]
            )
    buttons.append(
        [
            InlineKeyboardButton(
                text="< Back",
                callback_data=f"return_to_category_{media_count + 2}_{category_id}",
            )
        ]
    )
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def return_to_project_keyboard(
    media_count: int, project_id: int
) -> InlineKeyboardMarkup:
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.button(
        text="< Back", callback_data=f"return_to_project_{media_count + 2}_{project_id}"
    )
    keyboard_builder.adjust(1, repeat=True)
    return keyboard_builder.as_markup()
