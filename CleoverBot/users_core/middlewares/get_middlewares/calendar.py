import datetime
from typing import Callable, Dict, Any, Awaitable
import logging

from db.models.posts import PostModel

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
        try:
            if event.data == "calendar" and not (context_data.get("curr_date")):
                await state.update_data(
                    curr_date=datetime.datetime.now(tz=datetime.timezone.utc)
                    .date()
                    .isoformat()
                )
                context_data = await state.get_data()
            else:
                loc_date = datetime.date.fromisoformat(context_data.get("curr_date"))
                if event.data == "next_date":
                    new_date = loc_date + datetime.timedelta(days=1)
                    await state.update_data(curr_date=new_date.isoformat())
                elif event.data == "back_date":
                    new_date = loc_date - datetime.timedelta(days=1)
                    await state.update_data(curr_date=new_date.isoformat())
                context_data = await state.get_data()
            async with session_maker() as session:
                async with session.begin():
                    curr_date = datetime.date.fromisoformat(
                        context_data.get("curr_date")
                    )
                    res: ScalarResult = await session.execute(
                        select(PostModel).where(PostModel.start_date == curr_date)
                    )
                    posts = res.unique().scalars().all()
                    events = []
                    for event_news in posts:
                        events.append(
                            [
                                event_news.title,
                                event_news.short_description,
                                event_news.id,
                            ]
                        )
                    data["events_news"] = events
            return await handler(event, data)
        except Exception as e:
            logging.error(e)


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
                        PostModel.id == int(event.data.split("_")[-1])
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
                    "media": post.media,
                    "media_type": post.media_type,
                }
                data["event_datails"] = event_datails
        return await handler(event, data)
