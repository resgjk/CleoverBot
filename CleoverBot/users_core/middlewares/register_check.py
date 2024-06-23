from typing import Callable, Dict, Any, Awaitable
from datetime import datetime

from db.models.users import UserModel
from db.models.activities import ActivityModel

from aiogram import BaseMiddleware
from aiogram.types import Message

from sqlalchemy.orm import sessionmaker
from sqlalchemy import select
from sqlalchemy.engine import ScalarResult


class RegisterCheckMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any],
    ) -> Any:
        session_maker: sessionmaker = data["session_maker"]
        async with session_maker() as session:
            async with session.begin():
                res: ScalarResult = await session.execute(
                    select(UserModel).where(UserModel.user_id == event.from_user.id)
                )
                current_user: UserModel = res.scalars().one_or_none()

                if current_user:
                    data["is_subscriber"] = current_user.is_subscriber
                else:
                    activity_res: ScalarResult = await session.execute(
                        select(ActivityModel).where(ActivityModel.for_all)
                    )
                    activities: list[ActivityModel] = activity_res.scalars().all()
                    new_user = UserModel(
                        user_id=event.from_user.id,
                        is_subscriber=True,
                        subscriber_until=datetime(year=2024, month=12, day=30).date(),
                    )
                    # new_user = UserModel(user_id=event.from_user.id)
                    new_user.activities += activities
                    session.add(new_user)
                    await session.commit()
                    data["is_subscriber"] = True
                    # data["is_subscriber"] = False
        return await handler(event, data)
