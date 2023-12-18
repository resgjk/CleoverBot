from users_core.utils.phrases import phrases
from users_core.keyboards.return_to_main_keyboard import get_keyboard

from aiogram import Bot, Router, F
from aiogram.types import CallbackQuery


instruction_router = Router()


async def get_instruction(call: CallbackQuery, bot: Bot):
    await call.message.edit_text(
        text=phrases["instruction_text"], reply_markup=get_keyboard()
    )


instruction_router.callback_query.register(get_instruction, F.data == "instruction")
