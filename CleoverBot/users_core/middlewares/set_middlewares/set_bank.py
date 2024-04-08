from db.models.users import UserModel


from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery

from sqlalchemy.orm import sessionmaker
from sqlalchemy import select
from sqlalchemy.engine import ScalarResult


callbacks_data = {
    "set_bank_empty": "Zero bank",
    "set_bank_low": "$100 - 1000",
    "set_bank_middle": "$1000 - 10000",
    "set_bank_high": "$10k+",
}


class SetBankMiddleware(BaseMiddleware):
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
                current_user.bank = callbacks_data[event.data]
                data["choise_bank"] = current_user.bank
                await session.commit()
        return await handler(event, data)
