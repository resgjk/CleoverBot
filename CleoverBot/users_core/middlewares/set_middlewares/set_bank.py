from typing import Callable, Dict, Any, Awaitable
import logging

from db.models.users import UserModel

from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery

from sqlalchemy.orm import sessionmaker
from sqlalchemy import select, func
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
                if callbacks_data[event.data] in current_user.bank:
                    print(current_user.bank)
                    try:
                        temp_arr = current_user.bank[::]
                        temp_arr.remove(callbacks_data[event.data])
                        current_user.bank = temp_arr
                    except ValueError as e:
                        logging.error(e)
                else:
                    current_user.bank = current_user.bank + [callbacks_data[event.data]]
                await session.commit()
                data["choise_bank"] = current_user.bank
        return await handler(event, data)
