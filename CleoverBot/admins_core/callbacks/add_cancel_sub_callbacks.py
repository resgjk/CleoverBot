from admins_core.utils.phrases import phrases
from admins_core.utils.route_users_subs import UserSubscribeRoute
from admins_core.middlewares.subscribe_middlewares.get_end_date_for_add_sub import (
    GetEndDateForAddSubMiddleware,
)
from admins_core.keyboards.return_to_user_settings_keyboard import (
    return_to_user_settings_keyboard,
)
from admins_core.middlewares.subscribe_middlewares.get_id_for_delete_sub import (
    GetIdForDeleteSubMiddleware,
)

from aiogram import Bot, Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext


add_cancel_sub_router = Router()
get_id_for_add_sub_router = Router()
get_end_date_for_add_sub_router = Router()
delete_sub_router = Router()


async def add_sub(call: CallbackQuery, bot: Bot, state: FSMContext):
    await call.answer()
    await call.message.answer(text=phrases["add_sub_to_user"] + phrases["ps_id"])
    await state.set_state(UserSubscribeRoute.GET_ID_FOR_ADD_SUB)


async def get_id_for_add_sub(message: Message, bot: Bot, state: FSMContext):
    if message.text.isdigit():
        await state.update_data(user_id=int(message.text))
        await message.answer(text=phrases["add_sub_end_date"])
        await state.set_state(UserSubscribeRoute.GET_END_DATE_FOR_SUB)
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


async def cancel_sub(call: CallbackQuery, bot: Bot, state: FSMContext):
    await call.answer()
    await call.message.answer(text=phrases["cancel_sub_to_user"] + phrases["ps_id"])
    await state.set_state(UserSubscribeRoute.GET_ID_FOR_DELETE_SUB)


async def get_id_for_delete_sub(
    message: Message, bot: Bot, state: FSMContext, result: str
):
    if result == "success":
        text = f"✅ У пользователя {message.text} успешно отменена подписка"
        await state.clear()
        await message.answer(text=text, reply_markup=return_to_user_settings_keyboard())
    elif result == "invalid_user_id":
        await message.answer(text="Введите корректный ID пользователя:")
    elif result == "not_in_db":
        await message.answer(
            text="Пользователя с таким ID нет в базе данных. Введите ID еще раз:"
        )
    elif result == "user_dont_has_sub":
        text = f"Пользователь {message.text} не имеет подписки"
        await state.clear()
        await message.answer(text=text, reply_markup=return_to_user_settings_keyboard())


add_cancel_sub_router.callback_query.register(add_sub, F.data == "give_subscribe")
add_cancel_sub_router.callback_query.register(cancel_sub, F.data == "cancel_subscribe")

get_id_for_add_sub_router.message.register(
    get_id_for_add_sub, UserSubscribeRoute.GET_ID_FOR_ADD_SUB
)

get_end_date_for_add_sub_router.message.register(
    get_end_date_for_add_sub, UserSubscribeRoute.GET_END_DATE_FOR_SUB
)
get_end_date_for_add_sub_router.message.middleware.register(
    GetEndDateForAddSubMiddleware()
)

delete_sub_router.message.register(
    get_id_for_delete_sub, UserSubscribeRoute.GET_ID_FOR_DELETE_SUB
)
delete_sub_router.message.middleware.register(GetIdForDeleteSubMiddleware())
