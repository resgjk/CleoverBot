import base64
from datetime import datetime

from users_core.utils.phrases import phrases
from db.models.users import UserModel
from db.models.transactions import TransactionModel
from db.models.agency_stats import AgencyStatModel

from aiogram import Bot

from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine import ScalarResult
from sqlalchemy import select


def base64_to_int(base64_str: str):
    return int(base64.b64decode(base64_str).decode("utf-8"))


def int_to_base64(num: int):
    return base64.b64encode(str(num).encode("utf-8")).decode("utf-8")


async def send_notification_about_new_referral(user_id: int, bot: Bot):
    await bot.send_message(chat_id=user_id, text=phrases["new_referral_notification"])


async def add_agency_statistics(
    session_maker: sessionmaker, user_id: int, transaction_id: int
):
    async with session_maker() as session:
        async with session.begin():
            new_stat = AgencyStatModel(
                user_id=user_id,
                transaction_id=transaction_id,
                payment_datetime=datetime.now(),
            )
            session.add(new_stat)
            await session.commit()


async def replenish_referral_account(
    session_maker: sessionmaker, referral_link: str, transaction: TransactionModel
):
    print(base64_to_int(referral_link))
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
                    current_referral.referral_balance += transaction.amount * 0.1
                else:
                    current_referral.referral_balance += transaction.amount * 0.25
                    if current_referral.referral_status == "AGENCY":
                        await add_agency_statistics(
                            session_maker, current_referral.id, transaction.id
                        )
                await session.commit()
