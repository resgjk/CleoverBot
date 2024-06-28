from users_core.utils.phrases import phrases
from users_core.keyboards.referral_system_keyboard import get_referral_system_keyboard
from users_core.middlewares.get_middlewares.referral_system import (
    ReferralSystemMiddleware,
)

from aiogram import Bot, Router, F
from aiogram.types import CallbackQuery, FSInputFile, InputMediaPhoto


referral_system_router = Router()


async def get_referral_menu(call: CallbackQuery, bot: Bot, referral_details: dict):
    text = []
    link = f"https://t.me/cleover_test_bot?start={referral_details["link"]}"
    text.append(f'🔗 Your referral link: <b><a href="{link}">{link}</a></b>')
    text.append(
        f"🚶 You've attracted <b>{referral_details["referral_count"]}</b> referrals"
    )
    text.append(f"💵 Your balance: <b>{referral_details["balance"]}$</b>")

    media = InputMediaPhoto(
        media=FSInputFile("users_core/utils/photos/referral.png"),
        caption=phrases["referral_system"] + "\n\n".join(text),
    )
    await call.message.edit_media(
        media=media,
        reply_markup=get_referral_system_keyboard(),
    )


referral_system_router.callback_query.register(
    get_referral_menu, F.data == "referral_system"
)
referral_system_router.callback_query.middleware.register(ReferralSystemMiddleware())
