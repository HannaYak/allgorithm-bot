import asyncio
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from config import BOT_TOKEN
from database import init

from handlers.start import router as start_router
from handlers.registration import router as reg_router
from handlers.events import router as events_router
from handlers.admin import router as admin_router

# НОВЫЙ СПОСОБ ДЛЯ aiogram 3.13+
bot = Bot(
    token=BOT_TOKEN,
    default=DefaultBotProperties(parse_mode="HTML")
)
dp = Dispatcher()

async def main():
    await init()
    dp.include_router(start_router)
    dp.include_router(reg_router)
    dp.include_router(events_router)
    dp.include_router(admin_router)
    
    print("Бот запущен и работает 24/7!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
