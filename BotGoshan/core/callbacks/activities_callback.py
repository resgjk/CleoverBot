from core.utils.phrases import phrases
from core.keyboards.activities_keyboard import get_activities_keyboard

from aiogram import Bot, Router, F
from aiogram.types import CallbackQuery


activities_router = Router()


async def get_activities(call: CallbackQuery, bot: Bot):
    await call.message.edit_text(text=phrases["activities_text"])
    # await call.message.answer(text=" ", reply_markup=get_activities_keyboard())


activities_router.callback_query.register(get_activities, F.data == "activities")
