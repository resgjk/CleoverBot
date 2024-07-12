from typing import Callable, Dict, Any, Awaitable
from datetime import datetime
import logging
import base64

from db.models.users import UserModel
from db.models.activities import ActivityModel
from users_core.utils.referral_system_utils import (
    send_notification_about_new_referral,
    base64_to_int,
)
from users_core.config import TG_CHANNEL_ID

from aiogram import BaseMiddleware
from aiogram.types import (
    Message,
    CallbackQuery,
)
from aiogram.enums.chat_member_status import ChatMemberStatus

from sqlalchemy.orm import sessionmaker
from sqlalchemy import select
from sqlalchemy.engine import ScalarResult


class RegisterCheckMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message | CallbackQuery,
        data: Dict[str, Any],
    ) -> Any:
        session_maker: sessionmaker = data["session_maker"]
        async with session_maker() as session:
            async with session.begin():
                res: ScalarResult = await session.execute(
                    select(UserModel).where(UserModel.user_id == event.from_user.id)
                )
                current_user: UserModel = res.scalars().one_or_none()

                if current_user:
                    if (
                        isinstance(event, CallbackQuery)
                        and event.data == "check_channels"
                    ):
                        bot = data["bot"]
                        user_channel_status = await bot.get_chat_member(
                            chat_id=TG_CHANNEL_ID, user_id=current_user.user_id
                        )
                        current_user.is_in_channel = user_channel_status.status in [
                            ChatMemberStatus.MEMBER,
                            ChatMemberStatus.ADMINISTRATOR,
                            ChatMemberStatus.CREATOR,
                        ]
                        await session.commit()
                    data["is_subscriber"] = current_user.is_subscriber
                    data["in_channel"] = current_user.is_in_channel
                else:
                    activity_res: ScalarResult = await session.execute(
                        select(ActivityModel).where(ActivityModel.for_all)
                    )
                    activities: list[ActivityModel] = activity_res.scalars().all()
                    new_user = UserModel(
                        user_id=event.from_user.id,
                        username=event.from_user.username,
                        is_subscriber=True,
                        subscriber_until=datetime(year=2024, month=12, day=30).date(),
                    )
                    start_command = event.text.split(" ")
                    if len(start_command) == 2:
                        try:
                            referral_user_id = base64_to_int(start_command[1])
                            referral_res: ScalarResult = await session.execute(
                                select(UserModel).where(
                                    UserModel.user_id == referral_user_id
                                )
                            )
                            current_referral: UserModel = (
                                referral_res.scalars().one_or_none()
                            )
                            if current_referral:
                                new_user.referral_link = start_command[1]
                                current_referral.referral_count += 1
                                await send_notification_about_new_referral(
                                    current_referral.user_id, data["bot"]
                                )
                        except Exception as e:
                            logging.error(e)
                    new_user.activities += activities
                    session.add(new_user)
                    await session.commit()
                    data["is_subscriber"] = new_user.is_subscriber
                    data["in_channel"] = None
        return await handler(event, data)
