import asyncio
import logging
from config import bot, dp
from database import init_db

from handlers import (
    start_router, profile_router, events_router, booking_router,
    payments_router, my_bookings_router, cabinet_router,
    rules_router, support_router, admin_router
)

for router in [start_router, profile_router, events_router, booking_router,
               payments_router, my_bookings_router, cabinet_router,
               rules_router, support_router, admin_router]:
    dp.include_router(router)

async def main():
    await init_db()
    await bot.delete_webhook(drop_pending_updates=True)
    print("Webhook убит. Polling запущен. Я ЖИВОЙ НАВСЕГДА!")

    # Запускаем polling
    task = asyncio.create_task(dp.start_polling(bot))

    # Держим контейнер живым вечно
    while True:
        await asyncio.sleep(3600)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
