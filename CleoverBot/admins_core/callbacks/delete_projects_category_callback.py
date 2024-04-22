from admins_core.utils.phrases import phrases
from admins_core.utils.category_form import CategoryDeleteField
from admins_core.keyboards.return_to_categories_route_menu import (
    return_to_categories_route_keyboard,
)
from admins_core.middlewares.projects_middlewares.delete_projects_category_middleware import (
    DeleteProjectsCategoryMiddleware,
)

from aiogram import Bot, Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext


start_delete_projects_category_router = Router()
delete_projects_category_router = Router()


async def start_delete_category(call: CallbackQuery, bot: Bot, state: FSMContext):
    await call.answer()
    await call.message.answer(text=phrases["get_projects_category_title"])
    await state.set_state(CategoryDeleteField.GET_TITLE)


async def get_category_title(
    message: Message, bot: Bot, state: FSMContext, result: str
):
    if result == "success":
        await message.answer(
            text="✅ Категория успешно удалена!",
            reply_markup=return_to_categories_route_keyboard(),
        )
        await state.clear()
    elif result == "not_in_db":
        await message.answer(
            text="Категории с таким названием не существует",
            reply_markup=return_to_categories_route_keyboard(),
        )
        await state.clear()
    elif result == "invalid":
        await message.answer(text="Неверный формат названия. Введите название еще раз:")


start_delete_projects_category_router.callback_query.register(
    start_delete_category, F.data == "delete_category"
)
delete_projects_category_router.message.register(
    get_category_title, CategoryDeleteField.GET_TITLE
)
delete_projects_category_router.message.middleware.register(
    DeleteProjectsCategoryMiddleware()
)
