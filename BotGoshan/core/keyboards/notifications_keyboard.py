from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_notifications_keyboard(choise_time) -> InlineKeyboardMarkup:
    buttons_texts = {
        "1 Hour": "✅ 1 Hour" if choise_time == "1 Hour" else "1 Hour",
        "3 Hours": "✅ 3 Hours" if choise_time == "3 Hours" else "3 Hours",
        "6 Hours": "✅ 6 Hours" if choise_time == "6 Hours" else "6 Hours",
        "12 Hours": "✅ 12 Hours" if choise_time == "12 Hours" else "12 Hours",
    }

    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.button(
        text=buttons_texts["1 Hour"], callback_data="set_hours_notification_1"
    )
    keyboard_builder.button(
        text=buttons_texts["3 Hours"], callback_data="set_hours_notification_3"
    )
    keyboard_builder.button(
        text=buttons_texts["6 Hours"], callback_data="set_hours_notification_6"
    )
    keyboard_builder.button(
        text=buttons_texts["12 Hours"], callback_data="set_hours_notification_12"
    )
    keyboard_builder.button(text="⬅️ Return to settings", callback_data="settings")
    keyboard_builder.adjust(1, repeat=True)
    return keyboard_builder.as_markup()
