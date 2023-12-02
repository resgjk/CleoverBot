import os
from dotenv import load_dotenv


load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
WEEK_ACCOUNT= os.getenv("WEEK_ACCOUNT")
MONTH_ACCOUNT= os.getenv("MONTH_ACCOUNT")
THREE_MONTH_ACCOUNT= os.getenv("THREE_MONTH_ACCOUNT")
YEAR_ACCOUNT= os.getenv("YEAR_ACCOUNT")