import asyncio
from aiogram import types
from config import bot, dp
from handlers import start, games, admin, payment  # ← твои хендлеры

# Регистрация хендлеров
dp.include_router(start.router)
dp.include_router(games.router)
dp.include_router(admin.router)
dp.include_router(payment.router)

async def main():
    print("Bot started!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
