from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from os import getenv

TOKEN = getenv("7801157571:AAE9aS4ZY0A_VLf4Dkt2RULAaqFLwxykWj8")
ADMIN_ID = 5456905649  # ← ТВОЙ ID
WEBHOOK_URL = getenv("https://chic-wisdom-bot.up.railway.app")  # https://chic-wisdom-bot.up.railway.app

bot = Bot(
    token=TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)
dp = Dispatcher()
