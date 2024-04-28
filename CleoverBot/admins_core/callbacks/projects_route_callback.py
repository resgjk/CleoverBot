from admins_core.utils.phrases import phrases
from admins_core.keyboards.projects_route_keyboard import get_projects_route_keyboard

from aiogram import Bot, Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext


projects_route_router = Router()


async def projects_route_menu(call: CallbackQuery, bot: Bot, state: FSMContext):
    await state.clear()
    await call.message.edit_text(
        text=phrases["projects_route_menu"], reply_markup=get_projects_route_keyboard()
    )


projects_route_router.callback_query.register(
    projects_route_menu, F.data == "projects_route"
)
