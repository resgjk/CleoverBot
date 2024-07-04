from admins_core.utils.phrases import phrases
from admins_core.middlewares.referral_midlewares.accept_withdraw_request_middleware import (
    AcceptWithdrawRequestMiddleware,
)

from aiogram import Bot, Router, F
from aiogram.types import CallbackQuery


accept_withdraw_request_router = Router()


async def accept_request(call: CallbackQuery, bot: Bot, result: str, user_id: int):
    await call.answer()
    if result == "success":
        await call.message.edit_text(text="✅ Заявка успешно выполнена!")
        await bot.send_message(
            chat_id=user_id,
            text="✅ Your withdrawal request has been <b>successfully processed</b>! Wait for the receipt of funds!",
        )
    elif result == "already_paid":
        await call.message.edit_text(text="🆗 Заявка уже выполнена!")
    elif result == "empty" or result == "error":
        await call.message.answer(text="🚫 Неизвестная ошибка!")


accept_withdraw_request_router.callback_query.register(
    accept_request, F.data.contains("accept_request")
)
accept_withdraw_request_router.callback_query.middleware.register(
    AcceptWithdrawRequestMiddleware()
)
