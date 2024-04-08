from db.models.users import UserModel
from db.models.activities import ActivityModel

from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery

from sqlalchemy.orm import sessionmaker, selectinload
from sqlalchemy import select
from sqlalchemy.engine import ScalarResult


class GetChoiseActivitiesMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[CallbackQuery, Dict[str, Any]], Awaitable[Any]],
        event: CallbackQuery,
        data: Dict[str, Any],
    ) -> Any:
        session_maker: sessionmaker = data["session_maker"]
        async with session_maker() as session:
            async with session.begin():
                choise_activities = {
                    "defi": False,
                    "airdrops": False,
                    "news": False,
                    "ido_ico": False,
                    "ambassador_programs": False,
                    "nft": False,
                }
                res: ScalarResult = await session.execute(
                    select(UserModel)
                    .options(
                        selectinload(UserModel.activities).load_only(
                            ActivityModel.title
                        )
                    )
                    .where(UserModel.user_id == event.from_user.id)
                )
                current_user: UserModel = res.scalars().one_or_none()
                for activity in current_user.activities:
                    if activity.title in choise_activities:
                        choise_activities[activity.title] = True
                data["choise_activities"] = choise_activities
        return await handler(event, data)
