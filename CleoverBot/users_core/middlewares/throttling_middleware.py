from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import (
    Message,
    CallbackQuery,
)
from aiogram.fsm.storage.redis import RedisStorage


class ThrottlingMiddleware(BaseMiddleware):
    def __init__(self, storage: RedisStorage):
        self.storage = storage

    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message | CallbackQuery,
        data: Dict[str, Any],
    ) -> Any:
        user = f"user{event.from_user.id}"
        check_user = await self.storage.redis.get(name=user)
        if check_user:
            if int(check_user.decode()) == 1:
                await self.storage.redis.set(name=user, value=0, ex=10)
                if isinstance(event, Message):
                    return await event.answer(
                        "⌛ You're turning too often, please wait <b>10 seconds!</b>"
                    )
                elif isinstance(event, CallbackQuery):
                    return await event.message.answer(
                        "⌛ You're turning too often, please wait <b>10 seconds!</b>"
                    )
            return
        await self.storage.redis.set(name=user, value=1, ex=10)
        return await handler(event, data)
