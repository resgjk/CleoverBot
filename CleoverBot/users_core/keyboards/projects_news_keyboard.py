from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def choise_project_news_keyboard(news: dict, page: str) -> InlineKeyboardMarkup:
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
    buttons.append([InlineKeyboardButton(text="< Back", callback_data=f"projects")])
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard
