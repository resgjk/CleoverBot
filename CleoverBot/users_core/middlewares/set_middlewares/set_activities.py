from typing import Callable, Dict, Any, Awaitable
import logging

from db.models.users import UserModel
from db.models.activities import ActivityModel

from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery

from sqlalchemy.orm import sessionmaker, selectinload
from sqlalchemy import select
from sqlalchemy.engine import ScalarResult


class SetActivitiesMiddleware(BaseMiddleware):
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

                activity_res: ScalarResult = await session.execute(
                    select(ActivityModel).where(
                        ActivityModel.id == int(event.data.split("_")[-1])
                    )
                )
                current_activity = activity_res.scalars().one_or_none()

                all_activities_res: ScalarResult = await session.execute(
                    select(ActivityModel).where(ActivityModel.for_all == False)
                )
                all_activities: list[ActivityModel] = all_activities_res.scalars().all()

                if current_activity in current_user.activities:
                    try:
                        current_user.activities.remove(current_activity)
                    except ValueError as e:
                        logging.error(e)
                else:
                    current_user.activities.append(current_activity)

                choice_activities = {}
                for activity in all_activities:
                    if activity in current_user.activities:
                        choice_activities[f"✅ {activity.title}"] = activity.id
                    else:
                        choice_activities[activity.title] = activity.id
                data["choice_activities"] = choice_activities
                await session.commit()
        return await handler(event, data)
