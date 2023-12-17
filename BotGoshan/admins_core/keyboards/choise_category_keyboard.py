from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def get_activities_keyboard() -> ReplyKeyboardMarkup:
    keyboard_builder = ReplyKeyboardBuilder()
    keyboard_builder.button(text="DeFi 📚")
    keyboard_builder.button(text="Airdrops 💸")
    keyboard_builder.button(text="News 🗞")
    keyboard_builder.button(text="IDO | ICO 🤑")
    keyboard_builder.button(text="Ambassador Programs 👥")
    keyboard_builder.button(text="NFT 🖼")
    keyboard_builder.adjust(1, repeat=True)
    return keyboard_builder.as_markup(
        resize_keyboard=True,
        one_time_keyboard=True,
        input_field_placeholder="Выберите категорию:",
    )
