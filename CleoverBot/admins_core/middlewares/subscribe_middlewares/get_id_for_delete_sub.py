from datetime import datetime

from db.models.users import UserModel
from admins_core.utils.route_users_subs import UserSubscribeRoute


from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from sqlalchemy.orm import sessionmaker
from sqlalchemy import select
from sqlalchemy.engine import ScalarResult


class GetIdForDeleteSubMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any],
    ) -> Any:
        session_maker: sessionmaker = data["session_maker"]
        async with session_maker() as session:
            async with session.begin():
                if event.text.isdigit():
                    res: ScalarResult = await session.execute(
                        select(UserModel).where(UserModel.user_id == int(event.text))
                    )
                    current_user: UserModel = res.scalars().one_or_none()
                    if current_user:
                        if not current_user.is_subscriber:
                            data["result"] = "user_dont_has_sub"
                        elif current_user.is_subscriber:
                            current_user.is_subscriber = False
                            current_user.subscriber_until = None
                            await session.commit()
                            data["result"] = "success"
                    else:
                        data["result"] = "not_in_db"
                else:
                    data["result"] = "invalid_user_id"
        return await handler(event, data)
