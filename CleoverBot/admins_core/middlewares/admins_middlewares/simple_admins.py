from db.models.admins import AdminModel


from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import Message

from sqlalchemy.orm import sessionmaker
from sqlalchemy import select
from sqlalchemy.engine import ScalarResult


class AddSimpleAdminMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any],
    ) -> Any:
        session_maker: sessionmaker = data["session_maker"]
        async with session_maker() as session:
            async with session.begin():
                try:
                    res: ScalarResult = await session.execute(
                        select(AdminModel).where(AdminModel.user_id == int(event.text))
                    )
                    current_admin: AdminModel = res.scalars().one_or_none()
                    if current_admin:
                        data["result"] = "in_db"
                    else:
                        new_admin: AdminModel = AdminModel(user_id=int(event.text))
                        session.add(new_admin)
                        await session.commit()
                        data["result"] = "success"
                except ValueError:
                    data["result"] = "invalid"
        return await handler(event, data)


class DeleteSimpleAdminMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any],
    ) -> Any:
        session_maker: sessionmaker = data["session_maker"]
        async with session_maker() as session:
            async with session.begin():
                try:
                    res: ScalarResult = await session.execute(
                        select(AdminModel).where(AdminModel.user_id == int(event.text))
                    )
                    current_admin: AdminModel = res.scalars().one_or_none()
                    if current_admin:
                        await session.delete(current_admin)
                        await session.commit()
                        data["result"] = "success"
                    else:
                        data["result"] = "not_in_db"
                except ValueError:
                    data["result"] = "invalid"
        return await handler(event, data)
