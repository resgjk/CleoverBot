from db.models.users import UserModel


from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery

from sqlalchemy.orm import sessionmaker
from sqlalchemy import select
from sqlalchemy.engine import ScalarResult


callbacks_data = {
    "set_activity_defi": "defi",
    "set_activity_airdrops": "airdrops",
    "set_activity_news": "news",
    "set_activity_ido_ico": "ido_ico",
    "set_activity_ambassador_programs": "ambassador_programs",
    "set_activity_nft": "nft",
}


class SetActivitiesMiddleware(BaseMiddleware):
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
                match event.data:
                    case "set_activity_defi":
                        current_user.defi_activity = not (current_user.defi_activity)
                    case "set_activity_airdrops":
                        current_user.airdrops_activity = not (
                            current_user.airdrops_activity
                        )
                    case "set_activity_news":
                        current_user.news_activity = not (current_user.news_activity)
                    case "set_activity_ido_ico":
                        current_user.ido_ico_activity = not (
                            current_user.ido_ico_activity
                        )
                    case "set_activity_ambassador_programs":
                        current_user.ambassador_programs_activity = not (
                            current_user.ambassador_programs_activity
                        )
                    case "set_activity_nft":
                        current_user.nft_activity = not (current_user.nft_activity)
                data["choise_activities"] = {
                    "defi": current_user.defi_activity,
                    "airdrops": current_user.airdrops_activity,
                    "news": current_user.news_activity,
                    "ido_ico": current_user.ido_ico_activity,
                    "ambassador_programs": current_user.ambassador_programs_activity,
                    "nft": current_user.nft_activity,
                }
                await session.commit()
        return await handler(event, data)
