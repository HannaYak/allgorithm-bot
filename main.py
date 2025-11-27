import os
from aiohttp import web
from aiogram.webhook.aiohttp_server import SimpleRequestHandler

from config import bot, dp
from database import init_db

# подключаем все роутеры
from handlers import (
    start_router, profile_router, events_router, booking_router,
    payments_router, my_bookings_router, cabinet_router,
    rules_router, support_router, admin_router
)

for r in [start_router, profile_router, events_router, booking_router,
          payments_router, my_bookings_router, cabinet_router,
          rules_router, support_router, admin_router]:
    dp.include_router(r)

async def on_startup(_):
    await init_db()
    url = os.getenv("WEBHOOK_URL")
    await bot.set_webhook(url)
    print(f"Webhook установлен: {url}")

app = web.Application()
SimpleRequestHandler(dispatcher=dp, bot=bot).register(app, path="/")
app.on_startup.append(on_startup)

# ← ЭТО САМОЕ ВАЖНОЕ ДЛЯ RAILWAY 2025
web.run_app(app, host="0.0.0.0", port=os.environ.get("PORT", 8000))
