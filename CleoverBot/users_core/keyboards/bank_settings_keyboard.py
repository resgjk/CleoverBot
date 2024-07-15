from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_bank_keyboard(choise_bank) -> InlineKeyboardMarkup:
    buttons_texts = {
        "Zero bank": "✅ Zero bank" if "Zero bank" in choise_bank else "Zero bank",
        "$100 - 1000": (
            "✅ $100 - 1000" if "$100 - 1000" in choise_bank else "$100 - 1000"
        ),
        "$1000 - 10000": (
            "✅ $1000 - 10000" if "$1000 - 10000" in choise_bank else "$1000 - 10000"
        ),
        "$10k+": "✅ $10k+" if "$10k+" in choise_bank else "$10k+",
    }

    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.button(
        text=buttons_texts["Zero bank"], callback_data="set_bank_empty"
    )
    keyboard_builder.button(
        text=buttons_texts["$100 - 1000"], callback_data="set_bank_low"
    )
    keyboard_builder.button(
        text=buttons_texts["$1000 - 10000"], callback_data="set_bank_middle"
    )
    keyboard_builder.button(text=buttons_texts["$10k+"], callback_data="set_bank_high")
    keyboard_builder.button(text="⬅️ Return to settings", callback_data="settings")
    keyboard_builder.adjust(1, repeat=True)
    return keyboard_builder.as_markup()
