import asyncio
import logging

from db.models.activities import ActivityModel
from users_core.utils.add_media_function import add_media

from aiogram import Bot

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
                .where(ActivityModel.title == post_details["category"])
            )
            current_activity: ActivityModel = activity_res.scalars().one_or_none()
            users_id = []
            if current_activity:
                for user in current_activity.users:
                    if user.is_subscriber and user.notification == notification:
                        if (
                            post_details["bank"] != "Любой бюджет"
                            and user.bank == post_details["bank"]
                        ):
                            users_id.append(user.user_id)
                        else:
                            users_id.append(user.user_id)
            if users_id:
                text = []
                text.append(f"<b>{post_details['title']}</b>")
                text.append(f"{post_details['full_description']}")
                text = "\n\n".join(text)

                media = add_media(
                    text=text,
                    photos=post_details["photos"],
                    videos=post_details["videos"],
                )

                tasks = []
                try:
                    for id in users_id:
                        if media:
                            task = bot.send_media_group(
                                chat_id=id,
                                media=media,
                            )
                            tasks.append(task)
                        else:
                            task = bot.send_message(chat_id=id, text=text)
                            tasks.append(task)
                    await asyncio.gather(*tasks, return_exceptions=True)
                except Exception as e:
                    logging.error(e)
