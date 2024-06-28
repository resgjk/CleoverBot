from users_core.utils.phrases import phrases

from aiogram import Bot


async def send_notification_about_new_referral(user_id: int, bot: Bot):
    await bot.send_message(chat_id=user_id, text=phrases["new_referral_notification"])
