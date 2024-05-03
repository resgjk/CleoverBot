from users_core.utils.phrases import phrases

from users_core.middlewares.payment_middlewares.create_invoice_middleware import (
    CreateInvoiceMiddleware,
)

from aiogram import Bot, Router, F
from aiogram.types import CallbackQuery


create_invoice_router = Router()


async def create_invoice(call: CallbackQuery, bot: Bot, link, create_status):
    await call.answer()
    if create_status == "success":
        await call.message.answer(f'🧾 <a href="{link}">Your subscription invoice</a>')
    else:
        await call.message.answer(phrases["error_create_payment"])


create_invoice_router.callback_query.register(
    create_invoice, F.data.contains("month_subscription")
)
create_invoice_router.callback_query.middleware.register(CreateInvoiceMiddleware())
