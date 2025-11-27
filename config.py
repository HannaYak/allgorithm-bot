from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from os import getenv

TOKEN = getenv("BOT_TOKEN")
ADMIN_ID = 5456905649  # ← ТВОЙ ID
WEBHOOK_URL = getenv("WEBHOOK_URL")  # https://chic-wisdom-bot.up.railway.app

bot = Bot(
    token=TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)
dp = Dispatcher()
