from db.models.admins import AdminModel


from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import Message

from sqlalchemy.orm import sessionmaker
from sqlalchemy import select
from sqlalchemy.engine import ScalarResult


class CheckAdminMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any],
    ) -> Any:
        session_maker: sessionmaker = data["session_maker"]
        async with session_maker() as session:
            async with session.begin():
                res: ScalarResult = await session.execute(
                    select(AdminModel).where(AdminModel.user_id == event.from_user.id)
                )
                current_admin: AdminModel = res.scalars().one_or_none()

                if current_admin:
                    data["is_admin"] = True
                    data["is_super_admin"] = current_admin.is_super_admin
                else:
                    data["is_admin"] = False
                    data["is_super_admin"] = False
        return await handler(event, data)
