from db.models.users import UserModel


from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import Message

from sqlalchemy.orm import sessionmaker
from sqlalchemy import select
from sqlalchemy.engine import ScalarResult


class RegisterCheckMiddleware(BaseMiddleware):
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
                    select(UserModel).where(UserModel.user_id == event.from_user.id)
                )
                current_user = res.one_or_none()

                if current_user:
                    await event.answer(f"USER IS REGISTERED {current_user}")
                else:
                    new_user = UserModel(user_id=event.from_user.id)
                    await session.merge(new_user)
                    await session.commit()
                    await event.answer("REGISTRATION IS SUCCESS")
        return await handler(event, data)
