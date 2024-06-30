import base64

from users_core.utils.phrases import phrases
from db.models.users import UserModel

from aiogram import Bot

from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine import ScalarResult


def base64_to_int(base64_str: str):
    return int(base64.b64decode(base64_str).decode("utf-8"))


def int_to_base64(num: int):
    return base64.b64encode(str(num).encode("utf-8")).decode("utf-8")


async def send_notification_about_new_referral(user_id: int, bot: Bot):
    await bot.send_message(chat_id=user_id, text=phrases["new_referral_notification"])


async def replenish_agency():
    pass


async def replenish_referral_account(
    session_maker: sessionmaker, referral_link: str, amount: int
):
    async with session_maker() as session:
        async with session.begin():
            referral_res: ScalarResult = await session.execute(
                select(UserModel).where(
                    UserModel.user_id == base64_to_int(referral_link)
                )
            )
            current_referral: UserModel = referral_res.scalars().one_or_none()
            if current_referral:
                if current_referral.referral_status == "RABOTYAGA":
                    current_referral.referral_balance += amount * 0.1
                else:
                    current_referral.referral_balance += amount * 0.25
                    if current_referral.referral_status == "AGENCY":
                        await replenish_agency()
                await session.commit()
