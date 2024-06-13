from typing import Callable, Dict, Any, Awaitable
from datetime import date, time

from db.models.activities import ActivityModel
from db.models.posts import PostModel

from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from sqlalchemy.orm import sessionmaker, selectinload
from sqlalchemy import select
from sqlalchemy.engine import ScalarResult

from apscheduler_di import ContextSchedulerDecorator


class SendPostMiddleware(BaseMiddleware):
    def __init__(self, scheduler: ContextSchedulerDecorator) -> None:
        self.scheduler = scheduler

    async def __call__(
        self,
        handler: Callable[[CallbackQuery, Dict[str, Any]], Awaitable[Any]],
        event: CallbackQuery,
        data: Dict[str, Any],
    ) -> Any:
        data["scheduler"] = self.scheduler
        session_maker: sessionmaker = data["session_maker"]
        state: FSMContext = data["state"]
        context_data = await state.get_data()
        category = context_data.get("category")
        bank = context_data.get("bank")
        title = context_data.get("title")
        owner_id = context_data.get("owner_id")
        start_date = context_data.get("start_date")
        start_time = context_data.get("start_time")
        end_date = context_data.get("end_date")
        end_time = context_data.get("end_time")
        short_description = context_data.get("short_description")
        full_description = context_data.get("full_description")
        media = context_data.get("media")
        media_type = context_data.get("media_type")
        users_id = []
        async with session_maker() as session:
            async with session.begin():
                if title:
                    activity_res: ScalarResult = await session.execute(
                        select(ActivityModel)
                        .options(selectinload(ActivityModel.users))
                        .where(ActivityModel.title == category)
                    )
                    current_activity: ActivityModel = (
                        activity_res.scalars().one_or_none()
                    )

                    new_post = PostModel(
                        owner_id=owner_id,
                        title=title,
                        category_id=current_activity.id,
                        bank=bank,
                        short_description=short_description,
                        full_description=full_description,
                    )
                    if start_date:
                        if start_time:
                            new_post.start_time = time.fromisoformat(start_time)
                        new_post.start_date = date.fromisoformat(start_date)
                    if end_date:
                        if end_time:
                            new_post.end_time = time.fromisoformat(end_time)
                        new_post.end_date = date.fromisoformat(end_date)
                    if media:
                        new_post.media = media
                    if media_type:
                        new_post.media_type = media_type
                    session.add(new_post)

                if current_activity:
                    for user in current_activity.users:
                        if user.user_id != owner_id and user.is_subscriber:
                            if bank != "Любой бюджет" and user.bank == bank:
                                users_id.append(user.user_id)
                            else:
                                users_id.append(user.user_id)
                data["users_id"] = users_id
                await session.commit()
        return await handler(event, data)
