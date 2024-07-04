import logging
from typing import Callable, Dict, Any, Awaitable

from db.models.withdrawal_requests import WithdrawRequestModel

from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from sqlalchemy.orm import sessionmaker, joinedload
from sqlalchemy import select
from sqlalchemy.engine import ScalarResult


class GetRequestDetailsMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[CallbackQuery, Dict[str, Any]], Awaitable[Any]],
        event: CallbackQuery,
        data: Dict[str, Any],
    ) -> Any:
        session_maker: sessionmaker = data["session_maker"]
        async with session_maker() as session:
            async with session.begin():
                request_res: ScalarResult = await session.execute(
                    select(WithdrawRequestModel)
                    .options(joinedload(WithdrawRequestModel.user))
                    .where(WithdrawRequestModel.id == int(event.data.split("_")[-1]))
                )
                request = request_res.scalars().one_or_none()
                if request:
                    data["request_details"] = request
                    data["sender_details"] = {
                        "username": request.user.username,
                        "user_id": request.user.user_id,
                    }
                    data["result"] = "success"
                else:
                    data["request_details"] = None
                    data["sender_details"] = None
                    data["result"] = "error"
        return await handler(event, data)
