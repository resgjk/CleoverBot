from users_core.config import API_KEY, SHOP_ID
from users_core.utils.phrases import phrases
from db.models.users import UserModel
from db.models.transactions import TransactionModel

import aiohttp
from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery

from sqlalchemy.orm import sessionmaker
from sqlalchemy import select
from sqlalchemy.engine import ScalarResult


class CreateInvoiceMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[CallbackQuery, Dict[str, Any]], Awaitable[Any]],
        event: CallbackQuery,
        data: Dict[str, Any],
    ) -> Any:
        await event.message.answer(phrases["wait_payment_text"])
        session_maker: sessionmaker = data["session_maker"]
        async with aiohttp.ClientSession() as session:
            headers = {
                "Authorization": f"Token {API_KEY}",
                "Content-Type": "application/json",
            }

            invoice_data = {
                "shop_id": SHOP_ID,
                "currency": "USD",
                "time_to_pay": {"hours": 0, "minutes": 30},
                "available_currencies": ["USDT_TRC20", "ETH", "BTC"],
            }

            params = {
                "locale": "en",
            }

            if "one" in event.data:
                invoice_data["amount"] = 12
                transaction_type = "one_month"
            elif "three" in event.data:
                invoice_data["amount"] = 30
                transaction_type = "three_month"
            elif "six" in event.data:
                invoice_data["amount"] = 55
                transaction_type = "six_month"
            elif "twelve" in event.data:
                invoice_data["amount"] = 90
                transaction_type = "twelve_month"

            async with session.post(
                url="https://api.cryptocloud.plus/v2/invoice/create",
                headers=headers,
                json=invoice_data,
                params=params,
            ) as response:
                response_body = await response.json()
                if response.status == 200:
                    link = response_body["result"]["link"]
                    create_status = "success"
                else:
                    link = ""
                    create_status = "fail"
                data["link"] = link
                data["create_status"] = create_status

                async with session_maker() as db_session:
                    async with db_session.begin():
                        res: ScalarResult = await db_session.execute(
                            select(UserModel).where(
                                UserModel.user_id == event.from_user.id
                            )
                        )
                        current_user: UserModel = res.scalars().one_or_none()
                        transaction: TransactionModel = TransactionModel(
                            uuid=response_body["result"]["uuid"],
                            type=transaction_type,
                            user_id=current_user.id,
                            is_success=False,
                        )
                        db_session.add(transaction)
                        await db_session.commit()
        return await handler(event, data)
