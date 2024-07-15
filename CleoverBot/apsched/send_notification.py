import asyncio
import logging
import os

from db.models.activities import ActivityModel

from aiogram import Bot
from aiogram.types import FSInputFile
from aiogram.exceptions import TelegramForbiddenError

from sqlalchemy.orm import sessionmaker, selectinload
from sqlalchemy import select
from sqlalchemy.engine import ScalarResult


async def send_notifications(
    bot: Bot, session_maker: sessionmaker, post_details: dict, notification: str
):
    users_id = []
    async with session_maker() as session:
        async with session.begin():
            activity_res: ScalarResult = await session.execute(
                select(ActivityModel)
                .options(selectinload(ActivityModel.users))
                .where(ActivityModel.id == post_details["category"])
            )
            current_activity: ActivityModel = activity_res.scalars().one_or_none()
            users_id = []
            if current_activity:
                for user in current_activity.users:
                    if user.is_subscriber and user.notification == notification:
                        if (
                            post_details["bank"] == "Любой бюджет"
                            or post_details["bank"] in user.bank
                        ):
                            users_id.append(user.user_id)
            if users_id:
                text = []
                text.append(f"<b>{post_details['title']}</b>")
                text.append(f"{post_details['full_description']}")
                text = "\n\n".join(text)

                if post_details["media"] and os.path.exists(post_details["media"]):
                    media = FSInputFile(post_details["media"])
                else:
                    media = None

                tasks = []
                try:
                    for id in users_id:
                        if media:
                            if post_details["media_type"] == "photo":
                                task = bot.send_photo(
                                    chat_id=id, photo=media, caption=text
                                )
                            elif post_details["media_type"] == "video":
                                task = bot.send_video(
                                    chat_id=id, video=media, caption=text
                                )
                            tasks.append(task)
                        else:
                            event_photo = FSInputFile(
                                "users_core/utils/photos/event.png"
                            )
                            task = bot.send_photo(
                                chat_id=id, photo=event_photo, caption=text
                            )
                            tasks.append(task)
                    for success_task in tasks:
                        try:
                            await success_task
                        except TelegramForbiddenError:
                            pass
                        await asyncio.sleep(0.04)
                except Exception as e:
                    logging.error(e)
