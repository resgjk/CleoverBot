import asyncio

from db.models.activities import ActivityModel

from aiogram import Bot
from aiogram.types import (
    InputMediaPhoto,
    InputMediaVideo,
    FSInputFile,
)

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
                    if post_details["bank"] != "Любой бюджет":
                        if (
                            user.is_subscriber
                            and user.bank == post_details["bank"]
                            and user.notification == notification
                        ):
                            users_id.append(user.user_id)
                    else:
                        if user.is_subscriber and user.notification == notification:
                            users_id.append(user.user_id)
            if users_id:
                text = []
                text.append(f"🗞️ <b>{post_details['title']}</b>\n\n")
                text.append(f"📜 {post_details['full_description']}\n\n")
                if post_details["start_date"]:
                    date = ".".join(post_details["start_date"].split("-")[::-1])
                    if post_details["start_time"]:
                        text.append(
                            f"🗓️ Start date: {date}, {post_details['start_date']}\n"
                        )
                    else:
                        text.append(f"🗓️ Start date: {date}\n")
                if post_details["end_date"]:
                    date = ".".join(post_details["end_date"].split("-")[::-1])
                    if post_details["end_time"]:
                        text.append(f"🏁 End date: {date}, {post_details['end_time']}")
                    else:
                        text.append(f"🏁 End date: {date}")
                text = "".join(text)

                media = []
                if post_details["photos"]:
                    for photo in post_details["photos"]:
                        if not media:
                            media.append(
                                InputMediaPhoto(
                                    type="photo",
                                    media=FSInputFile(path=photo),
                                    caption=text,
                                )
                            )
                        else:
                            media.append(
                                InputMediaPhoto(
                                    type="photo", media=FSInputFile(path=photo)
                                )
                            )
                if post_details["videos"]:
                    for video in post_details["videos"]:
                        if not media:
                            media.append(
                                InputMediaVideo(
                                    type="video",
                                    media=FSInputFile(path=video),
                                    caption=text,
                                )
                            )
                        else:
                            media.append(
                                InputMediaVideo(
                                    type="video", media=FSInputFile(path=video)
                                )
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
                    await asyncio.gather(*tasks)
                except Exception as e:
                    print(e)
