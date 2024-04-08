from users_core.utils.phrases import phrases
from users_core.keyboards.return_to_main_keyboard import get_keyboard

from aiogram import Bot, Router, F
from aiogram.types import CallbackQuery


feedback_router = Router()


async def get_feedback(call: CallbackQuery, bot: Bot):
    await call.message.edit_text(
        text=phrases["feedback_text"], reply_markup=get_keyboard()
    )


feedback_router.callback_query.register(get_feedback, F.data == "feedback")
