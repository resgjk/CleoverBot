import os

from aiogram import Bot

from dotenv import load_dotenv

from sqlalchemy.engine import URL

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.jobstores.redis import RedisJobStore
from apscheduler_di import ContextSchedulerDecorator


load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
WEBHOOK_DOMAIN = os.getenv("WEBHOOK_DOMAIN")
WEBHOOK_PATH = os.getenv("WEBHOOK_PATH")
SECRET_KEY = os.getenv("SECRET_KEY")
SHOP_ID = os.getenv("SHOP_ID")
API_KEY = os.getenv("API_KEY")
CALLBACK_PATH = os.getenv("CALLBACK_PATH")

ONE_MONTH_PRICE = int(os.getenv("ONE_MONTH_PRICE"))
THREE_MONTH_PRICE = int(os.getenv("THREE_MONTH_PRICE"))
SIX_MONTH_PRICE = int(os.getenv("SIX_MONTH_PRICE"))
TWELVE_MONTH_PRICE = int(os.getenv("TWELVE_MONTH_PRICE"))

bot = Bot(token=BOT_TOKEN)

postgres_url = URL.create(
    "postgresql+asyncpg",
    username=DB_USER,
    host=DB_HOST,
    database=DB_NAME,
    port=DB_PORT,
    password=DB_PASSWORD,
)

#jobstores = {
#    "default": RedisJobStore(jobs_key="dispatched_trips_jobs",
#                             run_times_key="dispatched_trips_running",
#                             host="localhost",
#                             db=2,
#                             port=6379)
#}
#scheduler = ContextSchedulerDecorator(AsyncIOScheduler(timezone="Etc/UTC", jobstores=jobstores))
#scheduler.ctx.add_instance(bot, declared_class=Bot)
scheduler = AsyncIOScheduler(timezone="Etc/UTC")
