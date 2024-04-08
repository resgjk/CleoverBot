from db.models.users import UserModel
from db.models.activities import ActivityModel


from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery

from sqlalchemy.orm import sessionmaker, selectinload
from sqlalchemy import select
from sqlalchemy.engine import ScalarResult


callbacks_data = {
    "set_activity_defi": "defi",
    "set_activity_airdrops": "airdrops",
    "set_activity_news": "news",
    "set_activity_ido_ico": "ido_ico",
    "set_activity_ambassador_programs": "ambassador_programs",
    "set_activity_nft": "nft",
}


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
                    .options(selectinload(UserModel.activities))
                    .where(UserModel.user_id == event.from_user.id)
                )
                current_user: UserModel = res.scalars().one_or_none()
                if len(event.data.split("_")) == 4:
                    choisen_activity = (
                        f"{event.data.split('_')[-2]}_{event.data.split('_')[-1]}"
                    )
                else:
                    choisen_activity = event.data.split("_")[-1]
                res_activity: ScalarResult = await session.execute(
                    select(ActivityModel)
                    .options(selectinload(ActivityModel.users))
                    .where(ActivityModel.title == choisen_activity)
                )
                current_activity: ActivityModel = res_activity.scalars().one_or_none()
                if current_activity in current_user.activities:
                    current_user.activities.remove(current_activity)
                else:
                    current_user.activities.append(current_activity)
                for activity in current_user.activities:
                    if activity.title in choise_activities:
                        choise_activities[activity.title] = True
                data["choise_activities"] = choise_activities
                await session.commit()
        return await handler(event, data)
