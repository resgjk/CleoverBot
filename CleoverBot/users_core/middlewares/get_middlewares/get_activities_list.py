from typing import Callable, Dict, Any, Awaitable
import logging

from db.models.activities import ActivityModel
from db.models.posts import PostModel

from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from sqlalchemy.orm import sessionmaker, joinedload
from sqlalchemy import select, desc
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


class GetCurrentActivityEventsMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[CallbackQuery, Dict[str, Any]], Awaitable[Any]],
        event: CallbackQuery,
        data: Dict[str, Any],
    ) -> Any:
        session_maker: sessionmaker = data["session_maker"]
        state: FSMContext = data["state"]
        context_data = await state.get_data()
        try:
            if "show_activity_events" in event.data:
                new_page = 0
                await state.update_data(
                    current_activity_id=int(event.data.split("_")[-1])
                )
            else:
                page = context_data.get("user_events_page")
                if "next_events_page" in event.data:
                    new_page = page + 1
                elif "back_events_page" in event.data:
                    if page > 0:
                        new_page = page - 1

            async with session_maker() as session:
                async with session.begin():
                    context_data = await state.get_data()
                    current_activity_id = context_data.get("current_activity_id")
                    if "show_activity_events" in event.data:
                        activity_res: ScalarResult = await session.execute(
                            select(ActivityModel).where(
                                ActivityModel.id == current_activity_id
                            )
                        )
                        current_activity: ActivityModel = (
                            activity_res.scalars().one_or_none()
                        )
                        data["current_activity"] = {
                            "title": current_activity.title,
                            "description": current_activity.description,
                        }

                    events_res: ScalarResult = await session.execute(
                        select(PostModel)
                        .options(joinedload(PostModel.category))
                        .where(PostModel.category_id == current_activity_id)
                        .order_by(desc(PostModel.create_date))
                        .offset(new_page * 5)
                        .limit(5)
                    )
                    current_events = events_res.unique().scalars().all()
                    if current_events:
                        events_dict = {}
                        for activity_event in current_events:
                            events_dict[activity_event.title] = str(activity_event.id)
                        if not new_page:
                            if len(current_events) < 5:
                                page = "one"
                            else:
                                page = "first"
                        else:
                            if len(current_events) < 5:
                                page = "last"
                            else:
                                page = "middle"
                        data["current_events"] = events_dict
                        data["is_full"] = True
                        data["page"] = page
                        await state.update_data(user_events_page=new_page)
                    else:
                        data["current_events"] = {}
                        data["is_full"] = False
                        data["page"] = ""
            return await handler(event, data)
        except TypeError as e:
            logging.error(e)
