from admins_core.middlewares.referral_middlewares.accept_withdraw_request_middleware import (
    AcceptWithdrawRequestMiddleware,
)
from admins_core.keyboards.choice_withdraw_requests_keyboard import (
    return_to_requests_keyboard,
)

from aiogram import Bot, Router, F
from aiogram.types import CallbackQuery


accept_withdraw_request_router = Router()


async def accept_request(call: CallbackQuery, bot: Bot, result: str, user_id: int):
    await call.answer()
    if result == "success":
        if "with_back" in call.data:
            await call.message.edit_text(
                text="✅ Заявка успешно выполнена!",
                reply_markup=return_to_requests_keyboard(),
            )
        else:
            await call.message.edit_text(text="✅ Заявка успешно выполнена!")
        await bot.send_message(
            chat_id=user_id,
            text="✅ Your withdrawal request has been <b>successfully processed</b>! Wait for the receipt of funds!",
        )
    elif result == "already_paid":
        if "with_back" in call.data:
            await call.message.edit_text(
                text="🆗 Заявка уже выполнена!",
                reply_markup=return_to_requests_keyboard(),
            )
        else:
            await call.message.edit_text(text="🆗 Заявка уже выполнена!")
    elif result == "empty" or result == "error":
        if "with_back" in call.data:
            await call.message.edit_text(
                text="🚫 Неизвестная ошибка!",
                reply_markup=return_to_requests_keyboard(),
            )
        else:
            await call.message.answer(text="🚫 Неизвестная ошибка!")


accept_withdraw_request_router.callback_query.register(
    accept_request, F.data.contains("accept_request")
)
accept_withdraw_request_router.callback_query.middleware.register(
    AcceptWithdrawRequestMiddleware()
)
