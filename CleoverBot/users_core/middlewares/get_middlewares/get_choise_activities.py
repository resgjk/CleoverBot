from typing import Callable, Dict, Any, Awaitable

from db.models.users import UserModel
from db.models.activities import ActivityModel

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
                user_res: ScalarResult = await session.execute(
                    select(UserModel)
                    .options(selectinload(UserModel.activities))
                    .where(UserModel.user_id == event.from_user.id)
                )
                current_user: UserModel = user_res.scalars().one_or_none()

                activities_res: ScalarResult = await session.execute(
                    select(ActivityModel).where(ActivityModel.for_all == False)
                )
                current_activities: list[ActivityModel] = activities_res.scalars().all()

                choice_activities = {}
                for activity in current_activities:
                    if activity in current_user.activities:
                        choice_activities[f"✅ {activity.title}"] = activity.id
                    else:
                        choice_activities[activity.title] = activity.id
                data["choice_activities"] = choice_activities
        return await handler(event, data)
