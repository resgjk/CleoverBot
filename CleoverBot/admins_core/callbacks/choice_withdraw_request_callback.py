from admins_core.utils.phrases import phrases
from admins_core.keyboards.choice_withdraw_requests_keyboard import (
    choice_withdraw_request_keyboard,
    return_to_requests_keyboard,
)
from admins_core.keyboards.accept_withdraw_request import (
    get_accept_request_keyboard_with_back,
)
from admins_core.middlewares.withdraw_middlewares.get_requests import (
    GetRequestsMiddleware,
)
from admins_core.middlewares.withdraw_middlewares.get_request_details import (
    GetRequestDetailsMiddleware,
)

from db.models.withdrawal_requests import WithdrawRequestModel

from aiogram import Bot, Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext


choice_withdraw_request_router = Router()
get_request_details_router = Router()


async def choice_withdraw_request(
    call: CallbackQuery,
    bot: Bot,
    state: FSMContext,
    requests: dict,
    page: str,
    is_full: bool,
):
    await call.answer()
    if is_full:
        await call.message.edit_text(
            text=phrases["choice_withdraw_request"],
            reply_markup=choice_withdraw_request_keyboard(requests=requests, page=page),
        )


async def show_request_details(
    call: CallbackQuery,
    bot: Bot,
    state: FSMContext,
    request_details: WithdrawRequestModel,
    sender_details: dict,
    result: str,
):
    await call.answer()
    if result == "success":
        await call.message.edit_text(
            text=f"🆕 Заявка на вывод средств:\n<b>ID заявки</b>: <code>{request_details.uuid}</code>\n<b>Пользователь</b>: @{sender_details["username"]} <code>{sender_details["user_id"]}</code>\n<b>Кошелек</b>: <code>{request_details.wallet_address}</code>\n<b>Сумма</b>: <code>{request_details.amount}</code>",
            reply_markup=get_accept_request_keyboard_with_back(request_details.uuid),
        )
    elif result == "error":
        await call.message.edit_text(
            text="🚫 Данной заявки не существует!",
            reply_markup=return_to_requests_keyboard(),
        )


choice_withdraw_request_router.callback_query.register(
    choice_withdraw_request, F.data == "withdraw_request"
)
choice_withdraw_request_router.callback_query.register(
    choice_withdraw_request, F.data == "next_requests_page"
)
choice_withdraw_request_router.callback_query.register(
    choice_withdraw_request, F.data == "back_requests_page"
)
choice_withdraw_request_router.callback_query.middleware.register(
    GetRequestsMiddleware()
)
get_request_details_router.callback_query.register(
    show_request_details, F.data.contains("show_withdraw_request_")
)
get_request_details_router.callback_query.middleware.register(
    GetRequestDetailsMiddleware()
)
