from datetime import datetime, timezone
from typing import Callable, Dict, Any, Awaitable
import logging

from db.models.withdrawal_requests import WithdrawRequestModel

from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from sqlalchemy.orm import sessionmaker, joinedload
from sqlalchemy import select
from sqlalchemy.engine import ScalarResult


class AcceptWithdrawRequestMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[CallbackQuery, Dict[str, Any]], Awaitable[Any]],
        event: CallbackQuery,
        data: Dict[str, Any],
    ) -> Any:
        session_maker: sessionmaker = data["session_maker"]
        request_uuid = event.data.split("_")[-1]
        try:
            async with session_maker() as session:
                async with session.begin():
                    request_res: ScalarResult = await session.execute(
                        select(WithdrawRequestModel)
                        .options(joinedload(WithdrawRequestModel.user))
                        .where(WithdrawRequestModel.uuid == request_uuid)
                    )
                    current_request: WithdrawRequestModel = (
                        request_res.scalars().one_or_none()
                    )
                    if current_request:
                        if current_request.is_paid:
                            data["result"] = "already_paid"
                            data["user_id"] = 0
                        else:
                            current_request.user.referral_balance -= (
                                current_request.amount
                            )
                            current_request.is_paid = True
                            data["result"] = "success"
                            data["user_id"] = current_request.user.user_id
                            await session.commit()
                    else:
                        data["result"] = "empty"
                        data["user_id"] = 0
        except Exception as e:
            logging.error(e)
            data["result"] = "error"
            data["user_id"] = 0
        return await handler(event, data)
