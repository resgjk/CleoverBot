import asyncio

from db.models.withdrawal_requests import WithdrawRequestModel
from users_core.utils.phrases import phrases
from users_core.utils.withdrawal_form import WithdrawalForm
from users_core.keyboards.referral_system_keyboard import get_referral_system_keyboard
from admins_core.keyboards.accept_withdraw_request import get_accept_request_keyboard
from users_core.middlewares.get_middlewares.referral_system import (
    ReferralSystemMiddleware,
    GetWithdrawRequestMiddleware,
    GetWithdrawWalletMiddleware,
)

from aiogram import Bot, Router, F
from aiogram.types import CallbackQuery, FSInputFile, InputMediaPhoto, Message
from aiogram.fsm.context import FSMContext
from aiogram.exceptions import TelegramForbiddenError


referral_system_router = Router()
request_a_withdrawal_router = Router()
withdrawal_wallet_router = Router()


async def get_referral_menu(call: CallbackQuery, bot: Bot, referral_details: dict):
    text = []
    link = f"https://t.me/cleoverbot?start={referral_details["link"]}"
    text.append(f'🔗 Your referral link: <b><a href="{link}">{link}</a></b>')
    text.append(
        f"🚶 You've attracted <b>{referral_details["referral_count"]}</b> referrals"
    )
    text.append(f"💵 Your balance: <b>{referral_details["balance"]}$</b>")

    media = InputMediaPhoto(
        media=FSInputFile("users_core/utils/photos/referral.png"),
        caption=phrases["referral_system"] + "\n\n".join(text),
    )
    await call.message.edit_media(
        media=media,
        reply_markup=get_referral_system_keyboard(),
    )


async def get_request_a_withdrawal(
    call: CallbackQuery,
    bot: Bot,
    state: FSMContext,
    result: str,
):
    await call.answer()
    if result == "success":
        await call.message.answer(phrases["wallet_enter"])
        await state.set_state(WithdrawalForm.GET_WALLET_ADDRESS)
    elif result == "in_processing":
        await call.message.answer(phrases["withdrawal_in_process"])
    elif result == "insufficient_funds":
        await call.message.answer(phrases["insufficient_funds"])


async def get_withdrawal_wallet(
    message: Message,
    bot: Bot,
    state: FSMContext,
    request_details: WithdrawRequestModel,
    sender_details: dict,
    super_admins_ids: list,
    result: str,
):
    if result == "success":
        await message.answer(
            f"✅ Your request <code>{request_details.uuid}</code> of <b>{request_details.amount}$</b> has been successfully created! <b>Wait for fulfillment</b>!\n\n<b>P.S.</b> If you have any questions, write to support."
        )
        tasks = []
        for adm_id in super_admins_ids:
            task = bot.send_message(
                chat_id=adm_id,
                text=f"🆕 Заявка на вывод средств:\n<b>ID заявки</b>: <code>{request_details.uuid}</code>\n<b>Пользователь</b>: @{sender_details["username"]} <code>{sender_details["user_id"]}</code>\n<b>Кошелек</b>: <code>{request_details.wallet_address}</code>\n<b>Сумма</b>: <code>{request_details.amount}</code>",
                reply_markup=get_accept_request_keyboard(request_details.uuid),
            )
            tasks.append(task)
        for success_task in tasks:
            try:
                await success_task
            except TelegramForbiddenError:
                pass
            await asyncio.sleep(0.04)
    else:
        await message.answer(
            "🚫 It was not possible to process your request. Try again later!"
        )
    await state.clear()


referral_system_router.callback_query.register(
    get_referral_menu, F.data == "referral_system"
)
referral_system_router.callback_query.middleware.register(ReferralSystemMiddleware())
request_a_withdrawal_router.callback_query.register(
    get_request_a_withdrawal, F.data == "withdraw_money"
)
request_a_withdrawal_router.callback_query.middleware.register(
    GetWithdrawRequestMiddleware()
)
withdrawal_wallet_router.message.register(
    get_withdrawal_wallet, WithdrawalForm.GET_WALLET_ADDRESS
)
withdrawal_wallet_router.message.middleware.register(GetWithdrawWalletMiddleware())
