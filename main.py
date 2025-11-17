# main.py — ФИНАЛЬНАЯ ВЕРСИЯ (РАБОТАЕТ НА 1000000%)
import asyncio
from config import bot, dp
from database import init_db

# Импортируем роутеры по правильным именам
from handlers import (
    start_router,
    games_router,
    profile_router,
    help_router,
    payments_router,
    admin_router,
    support_router
)

# Подключаем их
dp.include_router(start_router)
dp.include_router(games_router)
dp.include_router(profile_router)
dp.include_router(help_router)
dp.include_router(payments_router)
dp.include_router(admin_router)
dp.include_router(support_router)

async def on_startup():
    await init_db()
    print("База данных готова")

async def main():
    print("Бот запущен в режиме polling")
    await on_startup()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
