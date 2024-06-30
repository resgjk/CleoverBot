from typing import Callable, Dict, Any, Awaitable
import base64

from db.models.users import UserModel
from users_core.utils.referral_system_utils import int_to_base64

from aiogram import BaseMiddleware
from aiogram.types import Message, ContentType

from sqlalchemy.orm import sessionmaker
from sqlalchemy import select
from sqlalchemy.engine import ScalarResult


class ReferralSystemMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any],
    ) -> Any:
        session_maker: sessionmaker = data["session_maker"]
        async with session_maker() as session:
            async with session.begin():
                user_res: ScalarResult = await session.execute(
                    select(UserModel).where(UserModel.user_id == event.from_user.id)
                )
                current_user: UserModel = user_res.scalars().one_or_none()
                referral_link = int_to_base64(current_user.user_id)
                data["referral_details"] = {
                    "link": referral_link,
                    "referral_count": current_user.referral_count,
                    "balance": current_user.referral_balance,
                }

        return await handler(event, data)
