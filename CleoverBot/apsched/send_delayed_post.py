import logging
import asyncio
from typing import Dict, Any, List
from datetime import date, time, datetime, timezone

from users_core.config import scheduler
from db.models.activities import ActivityModel
from db.models.posts import PostModel
from admins_core.utils.post_sender import PostSender

from aiogram import Bot
from aiogram.types import FSInputFile
from aiogram.exceptions import TelegramNetworkError, TelegramForbiddenError

from sqlalchemy.orm import sessionmaker, selectinload
from sqlalchemy import select
from sqlalchemy.engine import ScalarResult


async def save_delayed_post(
    context_data: Dict[str, Any],
    session_maker: sessionmaker,
) -> List[int]:
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
                    .where(ActivityModel.id == category)
                )
                current_activity: ActivityModel = activity_res.scalars().one_or_none()
                new_post = PostModel(
                    owner_id=owner_id,
                    create_date=datetime.now(tz=timezone.utc),
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
                        if bank == "Любой бюджет" or bank in user.bank:
                            users_id.append(user.user_id)
            await session.commit()
    return users_id


async def confirm_delayed_post(
    bot: Bot,
    context_data: Dict[str, Any],
    session_maker: sessionmaker,
):
    users_id = await save_delayed_post(
        context_data=context_data, session_maker=session_maker
    )
    if users_id:
        sender = PostSender(context_data=context_data)
        text, media = sender.send_post_to_users(scheduler=scheduler)
        media_type = context_data.get("media_type")

        tasks = []
        try:
            for id in users_id:
                if media:
                    try:
                        if media_type == "photo":
                            task = bot.send_photo(chat_id=id, photo=media, caption=text)
                        elif media_type == "video":
                            task = bot.send_video(chat_id=id, video=media, caption=text)
                    except TelegramNetworkError:
                        event_photo = FSInputFile("users_core/utils/photos/event.png")
                        task = bot.send_photo(
                            chat_id=id, photo=event_photo, caption=text
                        )
                else:
                    event_photo = FSInputFile("users_core/utils/photos/event.png")
                    task = bot.send_photo(chat_id=id, photo=event_photo, caption=text)
                tasks.append(task)
            for success_task in tasks:
                try:
                    await success_task
                except TelegramForbiddenError:
                    pass
                await asyncio.sleep(0.04)
        except Exception as e:
            logging.error(e)
