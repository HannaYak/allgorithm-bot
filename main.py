import asyncio
import logging
from config import bot, dp
from database import init_db

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
    await bot.delete_webhook(drop_pending_updates=True)
    print("Webhook убит. БОТ ЖИВОЙ НАВСЕГДА! 🔥")

    # Запускаем polling в фоне
    polling_task = asyncio.create_task(
        dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    )

    # Держим контейнер живым вечно
    try:
        while True:
            await asyncio.sleep(3600)   # спим час, Railway не убивает
    except asyncio.CancelledError:
        polling_task.cancel()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
