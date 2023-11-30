import asyncio

from config import BOT_TOKEN

from aiogram import Bot
from aiogram import Dispatcher
from aiogram import types


bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())