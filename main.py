import asyncio
import logging
from config import bot, dp
from database import init_db

# Все роутеры
from handlers import (
    start_router, profile_router, events_router, booking_router,
    payments_router, my_bookings_router, cabinet_router,
    rules_router, support_router, admin_router
)

dp.include_router(start_router)
dp.include_router(profile_router)
dp.include_router(events_router)
dp.include_router(booking_router)
dp.include_router(payments_router)
dp.include_router(my_bookings_router)
dp.include_router(cabinet_router)
dp.include_router(rules_router)
dp.include_router(support_router)
dp.include_router(admin_router)

async def on_startup(_):
    # ПРИНУДИТЕЛЬНО УБИВАЕМ ВЕБХУК ПРИ КАЖДОМ СТАРТЕ
    await bot.delete_webhook(drop_pending_updates=True)
    print("Вебхук принудительно удалён — теперь только polling!")

async def main():
    await init_db()
    await on_startup(None)
    print("Бот запущен — отвечает мгновенно!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
