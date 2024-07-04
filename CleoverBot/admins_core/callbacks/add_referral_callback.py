from admins_core.utils.phrases import phrases
from admins_core.utils.influencers_router import InfluencerRouter
from admins_core.keyboards.influencers_categories_keyboard import get_infl_type_keyboard
from admins_core.keyboards.return_to_user_settings_keyboard import (
    return_to_user_settings_keyboard,
)
from admins_core.middlewares.referral_middlewares.add_referral_middleware import (
    GetInfluencerIdMiddleware,
    GetInfluencerTypeMiddleware,
)

from aiogram import Bot, Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext


add_influencer_router = Router()
get_influencer_id_router = Router()
choice_influencer_type_router = Router()


async def add_influencer(call: CallbackQuery, bot: Bot, state: FSMContext):
    await call.answer()
    await call.message.answer(text=phrases["add_influencer"] + phrases["ps_id"])
    await state.set_state(InfluencerRouter.GET_ID_FOR_ADD_INFL)


async def get_id_for_add_influencer(
    message: Message, bot: Bot, state: FSMContext, result: str
):
    if result == "success":
        await state.update_data(user_id=int(message.text))
        await message.answer(
            text=phrases["get_infl_type"], reply_markup=get_infl_type_keyboard()
        )
        await state.update_data(infl_id=int(message.text))
        await state.set_state(InfluencerRouter.GET_INFL_TYPE)
    elif result == "not_in_db":
        await message.answer(
            text="Пользователя с таким ID не существует.",
            reply_markup=return_to_user_settings_keyboard(),
        )
    elif result == "invalid":
        await message.answer(text="Введите корректный ID пользователя:")


async def get_type_for_add_influencer(
    call: CallbackQuery, bot: Bot, state: FSMContext, result: str
):
    await call.answer()
    if result == "success":
        await call.message.answer(
            text="✅ Инфлюенсер успешно создан!",
            reply_markup=return_to_user_settings_keyboard(),
        )
    elif result == "already_has":
        await call.message.answer(
            text="⭕ Такой инфлюенсер уже существует!",
            reply_markup=return_to_user_settings_keyboard(),
        )


add_influencer_router.callback_query.register(
    add_influencer, F.data == "add_influencer"
)
get_influencer_id_router.message.register(
    get_id_for_add_influencer, InfluencerRouter.GET_ID_FOR_ADD_INFL
)
get_influencer_id_router.message.middleware.register(GetInfluencerIdMiddleware())
choice_influencer_type_router.callback_query.register(
    get_type_for_add_influencer,
    F.data == "average_infl",
    InfluencerRouter.GET_INFL_TYPE,
)
choice_influencer_type_router.callback_query.register(
    get_type_for_add_influencer, F.data == "agency_infl", InfluencerRouter.GET_INFL_TYPE
)
choice_influencer_type_router.callback_query.middleware.register(
    GetInfluencerTypeMiddleware()
)
