from users_core.utils.phrases import phrases
from users_core.keyboards.main_menu import (
    get_main_menu_keyboard_is_not_sub,
    get_main_menu_keyboard_is_sub,
)
from users_core.middlewares.register_check import RegisterCheckMiddleware

from aiogram import Bot, Router, F
from aiogram.types import CallbackQuery, FSInputFile, InputMediaPhoto
from aiogram.fsm.context import FSMContext

main_menu_router = Router()


async def return_to_main_menu(
    call: CallbackQuery, bot: Bot, is_subscriber: bool, state: FSMContext
):
    await state.clear()
    if is_subscriber:
        media = InputMediaPhoto(
            media=FSInputFile("users_core/utils/photos/menu.png"),
            caption=phrases["start_message"],
        )
        await call.message.edit_media(
            media=media,
            reply_markup=get_main_menu_keyboard_is_sub(),
        )
    else:
        media = InputMediaPhoto(
            media=FSInputFile("users_core/utils/photos/menu.png"),
            caption=phrases["start_message"],
        )
        await call.message.edit_media(
            media=media,
            reply_markup=get_main_menu_keyboard_is_not_sub(),
        )


main_menu_router.callback_query.register(
    return_to_main_menu, F.data == "return_to_main_menu"
)
main_menu_router.callback_query.middleware.register(RegisterCheckMiddleware())
