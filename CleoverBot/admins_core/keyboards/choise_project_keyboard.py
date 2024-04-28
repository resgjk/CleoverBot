from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def choise_project_keyboard(projects: dict, page: str) -> InlineKeyboardMarkup:
    buttons = []
    for project in projects.keys():
        buttons.append(
            [
                InlineKeyboardButton(
                    text=project,
                    callback_data=f"choise_project_for_view_{projects[project]}",
                )
            ]
        )

    match page:
        case "first":
            buttons.append(
                [InlineKeyboardButton(text="➡️", callback_data=f"next_projects_page")]
            )
        case "middle":
            buttons.append(
                [
                    InlineKeyboardButton(
                        text="⬅️", callback_data=f"back_projects_page"
                    ),
                    InlineKeyboardButton(
                        text="➡️", callback_data=f"next_projects_page"
                    ),
                ]
            )
        case "last":
            buttons.append(
                [InlineKeyboardButton(text="⬅️", callback_data=f"back_projects_page")]
            )
    buttons.append(
        [InlineKeyboardButton(text="🔙 Назад", callback_data=f"choise_project")]
    )
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard
