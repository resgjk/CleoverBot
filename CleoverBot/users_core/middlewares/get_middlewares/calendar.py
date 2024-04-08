from datetime import datetime, timedelta

from db.models.posts import PostModel

from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from sqlalchemy.orm import sessionmaker
from sqlalchemy import select
from sqlalchemy.engine import ScalarResult


class CalendarMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[CallbackQuery, Dict[str, Any]], Awaitable[Any]],
        event: CallbackQuery,
        data: Dict[str, Any],
    ) -> Any:
        session_maker: sessionmaker = data["session_maker"]
        state: FSMContext = data["state"]
        context_data = await state.get_data()
        if event.data == "calendar":
            await state.update_data(curr_date=str(datetime.now().date()))
            context_data = await state.get_data()
        else:
            loc_date = context_data.get("curr_date").split("-")
            datetime_date = datetime(
                day=int(loc_date[2]), month=int(loc_date[1]), year=int(loc_date[0])
            )
            if event.data == "next_date":
                new_date = datetime_date + timedelta(days=1)
            elif event.data == "back_date":
                new_date = datetime_date - timedelta(days=1)
            await state.update_data(curr_date=str(new_date.date()))
            context_data = await state.get_data()
        async with session_maker() as session:
            async with session.begin():
                curr_date = context_data.get("curr_date")
                res: ScalarResult = await session.execute(
                    select(PostModel).where(PostModel.start_date == curr_date)
                )
                posts = res.unique().scalars().all()
                events = []
                for event_news in posts:
                    events.append([event_news.title, event_news.short_description])
                data["events_news"] = events
        return await handler(event, data)


class GetEventDetails(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[CallbackQuery, Dict[str, Any]], Awaitable[Any]],
        event: CallbackQuery,
        data: Dict[str, Any],
    ) -> Any:
        session_maker: sessionmaker = data["session_maker"]
        async with session_maker() as session:
            async with session.begin():
                res: ScalarResult = await session.execute(
                    select(PostModel).where(
                        PostModel.title == event.data.split("_")[-1]
                    )
                )
                post: PostModel = res.scalars().one_or_none()
                event_datails = {
                    "title": post.title,
                    "start_date": post.start_date,
                    "start_time": post.start_time,
                    "end_date": post.end_date,
                    "end_time": post.end_time,
                    "full_description": post.full_description,
                    "photos": post.photos,
                    "videos": post.videos,
                }
                data["event_datails"] = event_datails
        return await handler(event, data)
