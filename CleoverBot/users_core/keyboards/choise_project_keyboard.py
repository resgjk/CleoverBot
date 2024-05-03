from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def choise_project_keyboard(
    projects: dict, page: str, category_id: int
) -> InlineKeyboardMarkup:
    buttons = []
    if projects:
        for project in projects.keys():
            if projects[project][1]:
                notification_btn_text = "<- 🔔"
                callback_text = "enable"
            else:
                notification_btn_text = "<- 🔕"
                callback_text = "disable"

            buttons.append(
                [
                    InlineKeyboardButton(
                        text=project,
                        callback_data=f"choise_project_for_user_view_{projects[project][0]}",
                    ),
                    InlineKeyboardButton(
                        text=notification_btn_text,
                        callback_data=f"{callback_text}_project_notification_for_user_{projects[project][0]}",
                    ),
                ]
            )

    match page:
        case "first":
            buttons.append(
                [
                    InlineKeyboardButton(
                        text="➡️",
                        callback_data=f"next_projects_page_for_user_choise_project",
                    )
                ]
            )
        case "middle":
            buttons.append(
                [
                    InlineKeyboardButton(
                        text="⬅️",
                        callback_data=f"back_projects_page_for_user_choise_project",
                    ),
                    InlineKeyboardButton(
                        text="➡️",
                        callback_data=f"next_projects_page_for_user_choise_project",
                    ),
                ]
            )
        case "last":
            buttons.append(
                [
                    InlineKeyboardButton(
                        text="⬅️",
                        callback_data=f"back_projects_page_for_user_choise_project",
                    )
                ]
            )
    if projects:
        buttons.append(
            [
                InlineKeyboardButton(
                    text="✅ Enable all notifications",
                    callback_data=f"enable_notifications_category_{category_id}",
                ),
            ]
        )
        buttons.append(
            [
                InlineKeyboardButton(
                    text="❌ Turn off all notifications",
                    callback_data=f"turn_off_notifications_category_{category_id}",
                ),
            ]
        )
    buttons.append([InlineKeyboardButton(text="< Back", callback_data=f"projects")])
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard
