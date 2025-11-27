from aiogram import Bot, Dispatcher
from os import getenv

TOKEN = getenv("BOT_TOKEN")
ADMIN_ID = 5456905649  # ← ТВОЙ ID
WEBHOOK_URL = getenv("WEBHOOK_URL")  # https://chic-wisdom-bot.up.railway.app

bot = Bot(token=TOKEN, parse_mode="HTML")
dp = Dispatcher()
