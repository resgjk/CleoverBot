from users_core.utils.phrases import phrases
from users_core.keyboards.return_to_main_keyboard import get_keyboard

from aiogram import Bot, Router, F
from aiogram.types import CallbackQuery, FSInputFile, InputMediaPhoto


feedback_router = Router()


async def get_feedback(call: CallbackQuery, bot: Bot):
    media = InputMediaPhoto(
        media=FSInputFile("users_core/utils/photos/feedback.png"),
        caption=phrases["feedback_text"],
    )
    await call.message.edit_media(media=media, reply_markup=get_keyboard())


feedback_router.callback_query.register(get_feedback, F.data == "feedback")
