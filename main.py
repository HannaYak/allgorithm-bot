import asyncio
import os
from aiohttp import web
from aiogram.webhook.aiohttp_server import SimpleRequestHandler

from config import bot, dp
from database import init_db

# ← ЭТО САМОЕ ГЛАВНОЕ — ПОДКЛЮЧЕНИЕ ВСЕХ РОУТЕРОВ
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

async def on_startup(app):
    await init_db()
    await bot.set_webhook(os.getenv("WEBHOOK_URL"))
    print(f"Webhook установлен: {os.getenv('WEBHOOK_URL')}")

app = web.Application()
SimpleRequestHandler(dispatcher=dp, bot=bot).register(app, path="/")
app.on_startup.append(on_startup)

if __name__ == "__main__":
    web.run_app(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))
