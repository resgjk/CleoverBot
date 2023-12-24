from datetime import datetime

from db.models.users import UserModel
from admins_core.utils.route_users_subs import UserSubscribeRoute


from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from sqlalchemy.orm import sessionmaker
from sqlalchemy import select
from sqlalchemy.engine import ScalarResult


class GetEndDateForAddSubMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any],
    ) -> Any:
        try:
            date = event.text.split(".")
            now_date = datetime.now()
            end_date = datetime(day=int(date[0]), month=int(date[1]), year=int(date[2]))
            if end_date > now_date:
                session_maker: sessionmaker = data["session_maker"]
                state: FSMContext = data["state"]
                context_data = await state.get_data()
                user_id = context_data.get("user_id")
                async with session_maker() as session:
                    async with session.begin():
                        res: ScalarResult = await session.execute(
                            select(UserModel).where(UserModel.user_id == user_id)
                        )
                        current_user: UserModel = res.scalars().one_or_none()
                        if current_user:
                            current_user.is_subscriber = True
                            current_user.subscriber_until = str(end_date.date())
                        else:
                            new_user = UserModel(user_id=user_id)
                            new_user.is_subscriber = True
                            new_user.subscriber_until = str(end_date.date())
                            session.add(new_user)
                        await session.commit()
                        data["result"] = "success"
                        await state.update_data(end_date=event.text)
            else:
                data["result"] = "low_date"
        except Exception:
            data["result"] = "invalid_date"
        return await handler(event, data)
