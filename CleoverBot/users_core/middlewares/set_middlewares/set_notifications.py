from typing import Callable, Dict, Any, Awaitable

from db.models.users import UserModel

from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery

from sqlalchemy.orm import sessionmaker
from sqlalchemy import select
from sqlalchemy.engine import ScalarResult


callbacks_data = {
    "set_hours_notification_1": "1 Hour",
    "set_hours_notification_3": "3 Hours",
    "set_hours_notification_6": "6 Hours",
    "set_hours_notification_12": "12 Hours",
}


class SetNotificationsMiddleware(BaseMiddleware):
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
                    select(UserModel).where(UserModel.user_id == event.from_user.id)
                )
                current_user: UserModel = res.scalars().one_or_none()
                current_user.notification = callbacks_data[event.data]
                data["choise_notification"] = current_user.notification
                await session.commit()
        return await handler(event, data)
