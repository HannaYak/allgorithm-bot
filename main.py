import asyncio
import os
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage

# БЕРЁМ ТОКЕН ПРЯМО ИЗ ПЕРЕМЕННОЙ RENDER
BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN не найден! Проверь переменные окружения в Render.")

bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode="HTML"))
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

# Подключаем все хендлеры
from handlers.start import router as start_router
from handlers.registration import router as reg_router
from handlers.events import router as events_router
from handlers.admin import router as admin_router

dp.include_router(start_router)
dp.include_router(reg_router)
dp.include_router(events_router)
dp.include_router(admin_router)

async def main():
    print("Бот запущен и работает 24/7!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
