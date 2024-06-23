from typing import Callable, Dict, Any, Awaitable

from db.models.activities import ActivityModel

from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery

from sqlalchemy.orm import sessionmaker
from sqlalchemy import select
from sqlalchemy.engine import ScalarResult


class GetActivitiesListMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[CallbackQuery, Dict[str, Any]], Awaitable[Any]],
        event: CallbackQuery,
        data: Dict[str, Any],
    ) -> Any:
        session_maker: sessionmaker = data["session_maker"]
        async with session_maker() as session:
            async with session.begin():
                activities_res: ScalarResult = await session.execute(
                    select(ActivityModel).where(ActivityModel.for_all == False)
                )
                current_activities: list[ActivityModel] = activities_res.scalars().all()

                activities = {}
                for activity in current_activities:
                    activities[activity.title] = activity.id
                data["activities"] = activities
        return await handler(event, data)
