from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import Message
from aiogram.fsm.storage.redis import RedisStorage


class ThrottlingMiddleware(BaseMiddleware):
    def __init__(self, limit: int, time_frame: int, storage: RedisStorage):
        self.limit = limit
        self.time_frame = time_frame
        self.storage = storage

    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any],
    ) -> Any:
        if event.text[0] == "/":
            user_id = event.from_user.id
            key = f"user:{user_id}"
            await self.storage.redis.incr(key)
            await self.storage.redis.expire(key, self.time_frame)
            curr_lim = await self.storage.redis.get(key)
            if int(curr_lim) > self.limit:
                await event.answer(
                    f"⌛ You're turning too often, please wait <b>{self.time_frame} seconds!</b>"
                )
                return
        return await handler(event, data)
