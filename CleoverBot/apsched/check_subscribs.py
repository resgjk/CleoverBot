from datetime import datetime, timezone
import asyncio

from db.models.users import UserModel
from users_core.utils.phrases import phrases
from users_core.keyboards.subscriptions_keyboard import get_buy_subscription_keyboard

from aiogram import Bot

from sqlalchemy.orm import sessionmaker
from sqlalchemy import select
from sqlalchemy.engine import ScalarResult


async def check_subscribs(bot: Bot, session_maker: sessionmaker):
    date = datetime.now(tz=timezone.utc).date()
    async with session_maker() as session:
        async with session.begin():
            res: ScalarResult = await session.execute(
                select(UserModel).where(UserModel.subscriber_until == date)
            )
            users: list[UserModel] = res.scalars().all()
            tasks = []
            for user in users:
                user.is_subscriber = False
                user.subscriber_until = None
                tasks.append(
                    bot.send_message(
                        chat_id=user.user_id,
                        text=phrases["sub_was_canceled"],
                        reply_markup=get_buy_subscription_keyboard(),
                    )
                )
            await session.commit()

            if tasks:
                await asyncio.gather(*tasks, return_exceptions=True)
