import asyncio
import logging
from config import bot, dp
from database import init_db

# Подключаем все роутеры
from handlers import (
    start_router, profile_router, events_router, booking_router,
    payments_router, my_bookings_router, cabinet_router,
    rules_router, support_router, admin_router
)

for r in [start_router, profile_router, events_router, booking_router,
          payments_router, my_bookings_router, cabinet_router,
          rules_router, support_router, admin_router]:
    dp.include_router(r)

async def main():
    await init_db()
    print("Бот запущен в режиме polling — отвечает мгновенно!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
