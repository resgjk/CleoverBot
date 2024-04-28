from admins_core.utils.phrases import phrases
from admins_core.keyboards.categories_route_keyboard import (
    get_categories_route_keyboard,
)

from aiogram import Bot, Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext


categories_route_router = Router()


async def categories_route_menu(call: CallbackQuery, bot: Bot, state: FSMContext):
    await state.clear()
    await call.message.edit_text(
        text=phrases["categories_route_menu"],
        reply_markup=get_categories_route_keyboard(),
    )


categories_route_router.callback_query.register(
    categories_route_menu, F.data == "categories_route"
)
