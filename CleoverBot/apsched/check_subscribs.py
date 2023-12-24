from datetime import datetime

from db.models.users import UserModel

from aiogram import Bot

from sqlalchemy.orm import sessionmaker
from sqlalchemy import select
from sqlalchemy.engine import ScalarResult


async def check_subscribs(bot: Bot, session_maker: sessionmaker):
    date = str(datetime.now().date())
    async with session_maker() as session:
        async with session.begin():
            res: ScalarResult = await session.execute(
                select(UserModel).where(UserModel.subscriber_until == date)
            )
            users: list[UserModel] = res.scalars().all()
            for user in users:
                user.is_subscriber = False
                user.subscriber_until = None
            await session.commit()
