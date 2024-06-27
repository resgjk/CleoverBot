from admins_core.utils.phrases import phrases
from admins_core.utils.influencers_router import InfluencerRouter
from admins_core.keyboards.influencers_categories_keyboard import get_infl_type_keyboard
from admins_core.keyboards.return_to_user_settings_keyboard import (
    return_to_user_settings_keyboard,
)

from aiogram import Bot, Router, F
from aiogram.types import CallbackQuery, Message, ContentType
from aiogram.fsm.context import FSMContext


add_influencer_router = Router()
choise_influencer_type_router = Router()


async def add_influencer(call: CallbackQuery, bot: Bot, state: FSMContext):
    await call.answer()
    await call.message.answer(text=phrases["add_influencer"] + phrases["ps_id"])
    await state.set_state(InfluencerRouter.GET_ID_FOR_ADD_INFL)


async def get_id_for_add_influencer(message: Message, bot: Bot, state: FSMContext):
    if message.content_type == ContentType.TEXT and message.text.isdigit():
        await state.update_data(user_id=int(message.text))
        await message.answer(text=phrases["get_infl_type"], reply_markup=get_infl_type_keyboard())
        await state.set_state(InfluencerRouter.GET_INFL_TYPE)
    else:
        await message.answer(text="Введите корректный ID пользователя:")


async def get_end_date_for_add_sub(
    message: Message, bot: Bot, state: FSMContext, result: str
):
    if result == "success":
        context_data = await state.get_data()
        user_id = context_data.get("user_id")
        end_date = context_data.get("end_date")
        text = f"✅ Пользователю {user_id} успешно добавлена подписка до {end_date}"
        await state.clear()
        await message.answer(text=text, reply_markup=return_to_user_settings_keyboard())
    elif result == "low_date":
        await message.answer(
            text="Дата должна быть больше <b>текущей даты</b>. Введите дату еще раз:"
        )
    elif result == "invalid_date":
        await message.answer(
            text="Неверный формат даты. Введите дату еще раз в формате <b>дд.мм.гггг</b> UTC"
        )

