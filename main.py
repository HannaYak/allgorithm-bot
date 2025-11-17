import asyncio
from aiogram import types
from config import bot, dp
from handlers import start, games, admin, payments

# === РЕГИСТРАЦИЯ ХЕНДЛЕРОВ ===
dp.include_router(start.router)
dp.include_router(games.router)
dp.include_router(admin.router)
dp.include_router(payments.router)

async def on_startup():
    await init_db()
    print("Database initialized")


async def main():
    print("Bot started! Polling mode.")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
