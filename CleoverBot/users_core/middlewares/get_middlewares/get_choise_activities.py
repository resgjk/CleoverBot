from db.models.users import UserModel


from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery

from sqlalchemy.orm import sessionmaker
from sqlalchemy import select
from sqlalchemy.engine import ScalarResult


class GetChoiseActivitiesMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[CallbackQuery, Dict[str, Any]], Awaitable[Any]],
        event: CallbackQuery,
        data: Dict[str, Any],
    ) -> Any:
        session_maker: sessionmaker = data["session_maker"]
        async with session_maker() as session:
            async with session.begin():
                res: ScalarResult = await session.execute(
                    select(UserModel).where(UserModel.user_id == event.from_user.id)
                )
                current_user: UserModel = res.scalars().one_or_none()
                data["choise_activities"] = {
                    "defi": current_user.defi_activity,
                    "airdrops": current_user.airdrops_activity,
                    "news": current_user.news_activity,
                    "ido_ico": current_user.ido_ico_activity,
                    "ambassador_programs": current_user.ambassador_programs_activity,
                    "nft": current_user.nft_activity,
                }
        return await handler(event, data)
