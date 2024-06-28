from datetime import datetime, timezone
from typing import Callable, Dict, Any, Awaitable

from db.models.users import UserModel

from aiogram import BaseMiddleware
from aiogram.types import Message, ContentType, CallbackQuery
from aiogram.fsm.context import FSMContext

from sqlalchemy.orm import sessionmaker
from sqlalchemy import select
from sqlalchemy.engine import ScalarResult


class GetInfluencerIdMidleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any],
    ) -> Any:
        session_maker: sessionmaker = data["session_maker"]
        if event.content_type == ContentType.TEXT and event.text.isdigit():
            async with session_maker() as session:
                async with session.begin():
                    res: ScalarResult = await session.execute(
                        select(UserModel).where(UserModel.user_id == int(event.text))
                    )
                    current_user: UserModel = res.scalars().one_or_none()
                    if current_user:
                        result = "success"
                    else:
                        result = "not_in_db"
        else:
            result = "invalid"
        data["result"] = result
        return await handler(event, data)


class GetInfluencerTypeMidleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[CallbackQuery, Dict[str, Any]], Awaitable[Any]],
        event: CallbackQuery,
        data: Dict[str, Any],
    ) -> Any:
        session_maker: sessionmaker = data["session_maker"]
        state: FSMContext = data["state"]
        context_data = await state.get_data()
        infl_types = {"average_infl": "INFLUENCER", "agency_infl": "AGENCY"}
        async with session_maker() as session:
            async with session.begin():
                res: ScalarResult = await session.execute(
                    select(UserModel).where(
                        UserModel.user_id == context_data.get("infl_id")
                    )
                )
                current_user: UserModel = res.scalars().one_or_none()
                if current_user.referral_status == infl_types[event.data]:
                    result = "already_has"
                else:
                    current_user.referral_status = infl_types[event.data]
                    result = "success"
                    await session.commit()

        data["result"] = result
        return await handler(event, data)
