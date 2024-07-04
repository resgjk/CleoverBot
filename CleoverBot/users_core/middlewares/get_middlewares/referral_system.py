from typing import Callable, Dict, Any, Awaitable
import base64
from uuid import uuid4
from datetime import datetime, timezone
import logging

from db.models.users import UserModel
from db.models.withdrawal_requests import WithdrawRequestModel
from db.models.admins import AdminModel
from users_core.utils.referral_system_utils import int_to_base64

from aiogram import BaseMiddleware
from aiogram.types import Message, ContentType, CallbackQuery

from sqlalchemy.orm import sessionmaker
from sqlalchemy import select
from sqlalchemy.engine import ScalarResult


class ReferralSystemMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[CallbackQuery, Dict[str, Any]], Awaitable[Any]],
        event: CallbackQuery,
        data: Dict[str, Any],
    ) -> Any:
        session_maker: sessionmaker = data["session_maker"]
        async with session_maker() as session:
            async with session.begin():
                user_res: ScalarResult = await session.execute(
                    select(UserModel).where(UserModel.user_id == event.from_user.id)
                )
                current_user: UserModel = user_res.scalars().one_or_none()
                referral_link = int_to_base64(current_user.user_id)
                data["referral_details"] = {
                    "link": referral_link,
                    "referral_count": current_user.referral_count,
                    "balance": current_user.referral_balance,
                }

        return await handler(event, data)


class GetWithdrawRequestMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[CallbackQuery, Dict[str, Any]], Awaitable[Any]],
        event: CallbackQuery,
        data: Dict[str, Any],
    ) -> Any:
        session_maker: sessionmaker = data["session_maker"]
        async with session_maker() as session:
            async with session.begin():
                user_res: ScalarResult = await session.execute(
                    select(UserModel).where(UserModel.user_id == event.from_user.id)
                )
                current_user: UserModel = user_res.scalars().one_or_none()
                if current_user.referral_balance >= 100:
                    request_res: ScalarResult = await session.execute(
                        select(WithdrawRequestModel).where(
                            WithdrawRequestModel.user_id == current_user.id,
                            WithdrawRequestModel.is_paid == False,
                        )
                    )
                    current_request: WithdrawRequestModel = (
                        request_res.scalars().one_or_none()
                    )
                    if current_request:
                        data["result"] = "in_processing"
                    else:
                        data["result"] = "success"
                else:
                    data["result"] = "insufficient_funds"

        return await handler(event, data)


class GetWithdrawWalletMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any],
    ) -> Any:
        session_maker: sessionmaker = data["session_maker"]
        result = "success"
        try:
            async with session_maker() as session:
                async with session.begin():
                    user_res: ScalarResult = await session.execute(
                        select(UserModel).where(UserModel.user_id == event.from_user.id)
                    )
                    current_user: UserModel = user_res.scalars().one_or_none()
                    new_request = WithdrawRequestModel(
                        uuid=str(uuid4()),
                        user_id=current_user.id,
                        create_datetime=datetime.now(tz=timezone.utc),
                        wallet_address=event.text,
                        amount=current_user.referral_balance,
                    )
                    session.add(new_request)
                    super_admins_res: ScalarResult = await session.execute(
                        select(AdminModel).where(AdminModel.is_super_admin)
                    )
                    super_admins: List[AdminModel] = super_admins_res.scalars().all()
                    data["request_details"] = new_request
                    data["super_admins_ids"] = [adm.user_id for adm in super_admins]
                    data["sender_details"] = {
                        "username": current_user.username,
                        "user_id": current_user.user_id,
                    }
                    await session.commit()
        except Exception as e:
            logging.error(e)
            result = "error"
            data["request_details"] = None
            data["super_admins_ids"] = None
            data["sender_details"] = None
        data["result"] = result

        return await handler(event, data)
