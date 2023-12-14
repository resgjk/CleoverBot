from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_activities_keyboard(choise_activities) -> InlineKeyboardMarkup:
    buttons_texts = {
        "defi": "✅ DeFi 📚" if choise_activities["defi"] else "DeFi 📚",
        "airdrops": "✅ Airdrops 💸" if choise_activities["airdrops"] else "Airdrops 💸",
        "news": "✅ News 🗞" if choise_activities["news"] else "News 🗞",
        "ido_ico": "✅ IDO | ICO 🤑" if choise_activities["ido_ico"] else "IDO | ICO 🤑",
        "ambassador_programs": "✅ Ambassador Programs 👥"
        if choise_activities["ambassador_programs"]
        else "Ambassador Programs 👥",
        "nft": "✅ NFT 🖼" if choise_activities["nft"] else "NFT 🖼",
    }

    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.button(
        text=buttons_texts["defi"], callback_data="set_activity_defi"
    )
    keyboard_builder.button(
        text=buttons_texts["airdrops"], callback_data="set_activity_airdrops"
    )
    keyboard_builder.button(
        text=buttons_texts["news"], callback_data="set_activity_news"
    )
    keyboard_builder.button(
        text=buttons_texts["ido_ico"], callback_data="set_activity_ido_ico"
    )
    keyboard_builder.button(
        text=buttons_texts["ambassador_programs"],
        callback_data="set_activity_ambassador_programs",
    )
    keyboard_builder.button(text=buttons_texts["nft"], callback_data="set_activity_nft")
    keyboard_builder.button(
        text="⬅️ Return to main menu", callback_data="return_to_main_menu"
    )
    keyboard_builder.adjust(1, repeat=True)
    return keyboard_builder.as_markup()
