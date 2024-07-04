import logging
from typing import Callable, Dict, Any, Awaitable

from db.models.withdrawal_requests import WithdrawRequestModel

from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from sqlalchemy.orm import sessionmaker
from sqlalchemy import select
from sqlalchemy.engine import ScalarResult


class GetRequestsMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[CallbackQuery, Dict[str, Any]], Awaitable[Any]],
        event: CallbackQuery,
        data: Dict[str, Any],
    ) -> Any:
        session_maker: sessionmaker = data["session_maker"]
        state: FSMContext = data["state"]
        context_data = await state.get_data()
        try:
            if "withdraw_request" in event.data:
                new_page = 0
                context_data = await state.get_data()
            else:
                page = context_data.get("requests_page")
                if "next_requests_page" in event.data:
                    new_page = page + 1
                elif "back_requests_page" in event.data:
                    if page > 0:
                        new_page = page - 1
                context_data = await state.get_data()

            async with session_maker() as session:
                async with session.begin():
                    requests_res: ScalarResult = await session.execute(
                        select(WithdrawRequestModel)
                        .where(WithdrawRequestModel.is_paid == False)
                        .offset(new_page * 5)
                        .limit(5)
                    )
                    requests = requests_res.unique().scalars().all()
                    if requests:
                        requests_dict = {}
                        for request in requests:
                            requests_dict[request.uuid] = str(request.id)
                        if not new_page:
                            if len(requests) < 5:
                                page = "one"
                            else:
                                page = "first"
                        else:
                            if len(requests) < 5:
                                page = "last"
                            else:
                                page = "middle"
                        data["requests"] = requests_dict
                        data["page"] = page
                        data["is_full"] = True
                        await state.update_data(requests_page=new_page)
                    else:
                        data["requests"] = {}
                        data["page"] = ""
                        data["is_full"] = False
            return await handler(event, data)
        except TypeError as e:
            logging.error(e)
