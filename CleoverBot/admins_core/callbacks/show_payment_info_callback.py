from admins_core.utils.phrases import phrases
from admins_core.keyboards.return_to_payment_info_keyboard import (
    return_to_payment_info_keyboard,
)
from aiogram import Bot, Router, F
from aiogram.types import CallbackQuery


show_payment_info_router = Router()


async def show_info(call: CallbackQuery, bot: Bot):
    data = call.data.split("_")[0]
    zatichka = (
        phrases["one_month_payment_info"]
        + phrases["three_month_payment_info"]
        + phrases["six_month_payment_info"]
        + phrases["twelve_month_payment_info"]
        + "\n\n<b>Итог:</b>\n- Продано подписок: 0 шт.\n- Заработано: 0$"
    )

    match data:
        case "one":
            text = "Информация за текущий месяц:" + zatichka
        case "three":
            text = "Информация за три месяца:" + zatichka
        case "six":
            text = "Информация за шесть месяцев:" + zatichka
        case "twelve":
            text = "Информация за текущий год:" + zatichka
        case "all":
            text = "Информация за все время:" + zatichka

    await call.message.edit_text(
        text=text, reply_markup=return_to_payment_info_keyboard()
    )


show_payment_info_router.callback_query.register(
    show_info, F.data.contains("month_info")
)
