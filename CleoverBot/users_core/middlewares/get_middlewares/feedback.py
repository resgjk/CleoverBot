from typing import Callable, Dict, Any, Awaitable

from db.models.admins import AdminModel

from aiogram import BaseMiddleware
from aiogram.types import Message

from sqlalchemy.orm import sessionmaker
from sqlalchemy import select
from sqlalchemy.engine import ScalarResult


class PostFeedbackMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any],
    ) -> Any:
        session_maker: sessionmaker = data["session_maker"]
        async with session_maker() as session:
            async with session.begin():
                res: ScalarResult = await session.execute(select(AdminModel))
                current_admins: list[AdminModel] = res.scalars().all()

                admin_ids = [admin.user_id for admin in current_admins]
                data["admin_ids"] = admin_ids

        return await handler(event, data)
