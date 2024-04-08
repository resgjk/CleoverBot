from admins_core.utils.phrases import phrases
from admins_core.keyboards.super_admins_settings_keyboard import (
    get_super_admins_settings_keyboard,
)
from admins_core.utils.super_admins_route import SuperAdminRoute
from admins_core.keyboards.return_to_super_admins_settings import (
    return_to_super_admins_keyboard,
)
from admins_core.middlewares.admins_middlewares.super_admins import (
    AddSuperAdminMiddleware,
    DeleteSuperAdminMiddleware,
)

from aiogram import Bot, Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext


super_admins_settings_router = Router()
add_super_admin_router = Router()
delete_super_admin_router = Router()


async def super_admins_settings(call: CallbackQuery, bot: Bot):
    await call.message.edit_text(
        text=phrases["simple_admins_settings"],
        reply_markup=get_super_admins_settings_keyboard(),
    )


async def start_add_super_admin(call: CallbackQuery, bot: Bot, state: FSMContext):
    await call.answer()
    await call.message.answer(text=phrases["add_super_admin"])
    await state.set_state(SuperAdminRoute.GET_ID_FOR_ADD_ADMIN)


async def start_delete_super_admin(call: CallbackQuery, bot: Bot, state: FSMContext):
    await call.answer()
    await call.message.answer(text=phrases["delete_super_admin"])
    await state.set_state(SuperAdminRoute.GET_ID_FOR_DELETE_ADMIN)


async def get_id_for_add_super_admin(
    message: Message, bot: Bot, state: FSMContext, result: str
):
    if result == "in_db":
        await message.answer(
            text="Супер - дминистратор с таким ID уже существует",
            reply_markup=return_to_super_admins_keyboard(),
        )
        await state.clear()
    elif result == "invalid":
        await message.answer(text="Неверный формат ID. Введите ID еще раз:")
    elif result == "success":
        await message.answer(
            text="✅ Супер - администратор успешно добавлен!",
            reply_markup=return_to_super_admins_keyboard(),
        )
        await state.clear()


async def get_id_for_delete_super_admin(
    message: Message, bot: Bot, state: FSMContext, result: str
):
    if result == "not_in_db":
        await message.answer(
            text="Супер - администратора с таким ID не существует",
            reply_markup=return_to_super_admins_keyboard(),
        )
        await state.clear()
    elif result == "invalid":
        await message.answer(text="Неверный формат ID. Введите ID еще раз:")
    elif result == "success":
        await message.answer(
            text="✅ Супер - администратор успешно удален!",
            reply_markup=return_to_super_admins_keyboard(),
        )
        await state.clear()


super_admins_settings_router.callback_query.register(
    super_admins_settings, F.data == "super_administrators"
)
super_admins_settings_router.callback_query.register(
    start_add_super_admin, F.data == "add_super_admin"
)
super_admins_settings_router.callback_query.register(
    start_delete_super_admin, F.data == "delete_super_admin"
)

add_super_admin_router.message.register(
    get_id_for_add_super_admin, SuperAdminRoute.GET_ID_FOR_ADD_ADMIN
)
add_super_admin_router.message.middleware.register(AddSuperAdminMiddleware())

delete_super_admin_router.message.register(
    get_id_for_delete_super_admin, SuperAdminRoute.GET_ID_FOR_DELETE_ADMIN
)
delete_super_admin_router.message.middleware.register(DeleteSuperAdminMiddleware())
