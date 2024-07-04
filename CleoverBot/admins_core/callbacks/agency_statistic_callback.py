import os

from admins_core.utils.phrases import phrases
from admins_core.keyboards.agency_statistics_keyboard import get_statistic_type_keyboard
from admins_core.utils.create_statistic_files import (
    get_transactions_document,
    get_users_document,
)

from sqlalchemy.orm import sessionmaker

from aiogram.types import CallbackQuery, FSInputFile
from aiogram import Bot, Router, F
from aiogram.fsm.context import FSMContext


agency_statistic_router = Router()


async def statistic_menu(call: CallbackQuery, bot: Bot, state: FSMContext):
    await state.clear()
    await call.message.edit_text(
        phrases["get_statistic_type"], reply_markup=get_statistic_type_keyboard()
    )


async def send_transactions_document(
    call: CallbackQuery, bot: Bot, state: FSMContext, session_maker: sessionmaker
):
    await call.answer()
    file_name = await get_transactions_document(session_maker)
    if file_name and os.path.exists(file_name):
        await bot.send_document(
            call.message.chat.id,
            document=FSInputFile(file_name),
            caption="✅ Статистика по транзакциям успешно создана!",
        )
        os.remove(file_name)
    else:
        await call.message.answer(
            text="🚫 Не удалось отправить статистику! Попробуйте позже!"
        )


async def send_users_document(
    call: CallbackQuery, bot: Bot, state: FSMContext, session_maker: sessionmaker
):
    await call.answer()
    file_name = await get_users_document(session_maker)
    if file_name and os.path.exists(file_name):
        await bot.send_document(
            call.message.chat.id,
            document=FSInputFile(file_name),
            caption="✅ Статистика по пользователям успешно создана!",
        )
        os.remove(file_name)
    else:
        await call.message.answer(
            text="🚫 Не удалось отправить статистику! Попробуйте позже!"
        )


agency_statistic_router.callback_query.register(
    statistic_menu, F.data == "agency_statistic"
)
agency_statistic_router.callback_query.register(
    send_transactions_document, F.data == "transactions_statistic"
)
agency_statistic_router.callback_query.register(
    send_users_document, F.data == "infl_statistic"
)
