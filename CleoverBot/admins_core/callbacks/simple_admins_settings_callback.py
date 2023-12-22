from admins_core.utils.phrases import phrases
from admins_core.keyboards.simple_admins_settings_keyboard import (
    get_simple_admins_settings_keyboard,
)
from admins_core.utils.simple_admins_route import SimpleAdminRoute
from admins_core.keyboards.return_to_simple_admins_settings import (
    return_to_simple_admins_keyboard,
)
from admins_core.middlewares.admins_middlewares.simple_admins import (
    AddSimpleAdminMiddleware,
    DeleteSimpleAdminMiddleware,
)

from aiogram import Bot, Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext


simple_admins_settings_router = Router()
add_simple_admin_router = Router()
delete_simple_admin_router = Router()


async def simple_admins_settings(call: CallbackQuery, bot: Bot):
    await call.message.edit_text(
        text=phrases["simple_admins_settings"],
        reply_markup=get_simple_admins_settings_keyboard(),
    )


async def start_add_simple_admin(call: CallbackQuery, bot: Bot, state: FSMContext):
    await call.answer()
    await call.message.answer(text=phrases["add_simple_admin"])
    await state.set_state(SimpleAdminRoute.GET_ID_FOR_ADD_ADMIN)


async def start_delete_simple_admin(call: CallbackQuery, bot: Bot, state: FSMContext):
    await call.answer()
    await call.message.answer(text=phrases["delete_simple_admin"])
    await state.set_state(SimpleAdminRoute.GET_ID_FOR_DELETE_ADMIN)


async def get_id_for_add_simple_admin(
    message: Message, bot: Bot, state: FSMContext, result: str
):
    if result == "in_db":
        await message.answer(
            text="Администратор с таким ID уже существует",
            reply_markup=return_to_simple_admins_keyboard(),
        )
        await state.clear()
    elif result == "invalid":
        await message.answer(text="Неверный формат ID. Введите ID еще раз:")
    elif result == "success":
        await message.answer(
            text="✅ Администратор успешно добавлен!",
            reply_markup=return_to_simple_admins_keyboard(),
        )
        await state.clear()


async def get_id_for_delete_simple_admin(
    message: Message, bot: Bot, state: FSMContext, result: str
):
    if result == "not_in_db":
        await message.answer(
            text="Администратора с таким ID не существует",
            reply_markup=return_to_simple_admins_keyboard(),
        )
        await state.clear()
    elif result == "invalid":
        await message.answer(text="Неверный формат ID. Введите ID еще раз:")
    elif result == "success":
        await message.answer(
            text="✅ Администратор успешно удален!",
            reply_markup=return_to_simple_admins_keyboard(),
        )
        await state.clear()


simple_admins_settings_router.callback_query.register(
    simple_admins_settings, F.data == "simple_administrators"
)
simple_admins_settings_router.callback_query.register(
    start_add_simple_admin, F.data == "add_simple_admin"
)
simple_admins_settings_router.callback_query.register(
    start_delete_simple_admin, F.data == "delete_simple_admin"
)

add_simple_admin_router.message.register(
    get_id_for_add_simple_admin, SimpleAdminRoute.GET_ID_FOR_ADD_ADMIN
)
add_simple_admin_router.message.middleware.register(AddSimpleAdminMiddleware())

delete_simple_admin_router.message.register(
    get_id_for_delete_simple_admin, SimpleAdminRoute.GET_ID_FOR_DELETE_ADMIN
)
delete_simple_admin_router.message.middleware.register(DeleteSimpleAdminMiddleware())
