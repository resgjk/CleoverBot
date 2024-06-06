import asyncio
import logging

from users_core.utils.phrases import phrases
from users_core.utils.feedback_form import FeedbackForm
from users_core.keyboards.return_to_main_keyboard import get_keyboard
from users_core.middlewares.get_middlewares.feedback import PostFeedbackMiddleware

from aiogram import Bot, Router, F
from aiogram.types import CallbackQuery, FSInputFile, InputMediaPhoto, Message
from aiogram.fsm.context import FSMContext


feedback_router = Router()


async def get_feedback(call: CallbackQuery, bot: Bot, state: FSMContext):
    media = InputMediaPhoto(
        media=FSInputFile("users_core/utils/photos/feedback.png"),
        caption=phrases["feedback_text"],
    )
    await call.message.edit_media(media=media, reply_markup=get_keyboard())
    await state.set_state(FeedbackForm.GET_FEEDBACK)


async def post_feedback(
    message: Message, bot: Bot, state: FSMContext, admin_ids: list, result: str
):
    if result == "success":
        feedback_photo = FSInputFile("users_core/utils/photos/feedback.png")
        await message.answer_photo(
            photo=feedback_photo,
            caption=phrases["user_post_feedback"],
            reply_markup=get_keyboard(),
        )
        await state.clear()

        if admin_ids:
            try:
                tasks = []
                for id in admin_ids:
                    task = bot.send_message(
                        chat_id=id, text=phrases["admin_show_feedback"] + message.text
                    )
                    tasks.append(task)
                await asyncio.gather(*tasks, return_exceptions=True)
            except Exception as e:
                logging.error(e)
    elif result == "invalid":
        await message.answer(text="🚫 Sorry, but you can only send text!")


feedback_router.callback_query.register(get_feedback, F.data == "feedback")
feedback_router.message.register(post_feedback, FeedbackForm.GET_FEEDBACK)
feedback_router.message.middleware.register(PostFeedbackMiddleware())
