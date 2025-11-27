import asyncio
import os
from aiohttp import web
from aiogram.webhook.aiohttp_server import SimpleRequestHandler

from config import bot, dp, WEBHOOK_URL
from database import init_db

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
    await init_db()
    await bot.set_webhook(WEBHOOK_URL)
    print(f"Webhook установлен: {WEBHOOK_URL}")

async def on_shutdown(_):
    await bot.delete_webhook(drop_pending_updates=True)
    await bot.session.close()

async def main():
    app = web.Application()
    SimpleRequestHandler(dispatcher=dp, bot=bot).register(app, path="/")
    app.on_startup.append(on_startup)
    app.on_shutdown.append(on_shutdown)

    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", int(os.environ.get("PORT", 8000)))
    await site.start()

    print("Бот запущен на Railway — живём вечно ❤️")
    while True:
        await asyncio.sleep(3600)

if __name__ == "__main__":
    asyncio.run(main())
