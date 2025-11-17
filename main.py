import asyncio
from config import bot, dp
from database import init_db

# Подключаем ВСЕ роутеры
from handlers import start, games, profile, help, payments, admin

dp.include_router(start.router)
dp.include_router(games.router)
dp.include_router(profile.router)
dp.include_router(help.router)
dp.include_router(payments.router)
dp.include_router(admin.router)   # это будет твой новый мощный admin.py

async def on_startup():
    await init_db()
    print("База данных инициализирована")

async def main():
    print("Бот запущен в режиме polling")
    await on_startup()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
