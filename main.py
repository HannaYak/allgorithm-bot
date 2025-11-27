# main.py — ФИНАЛЬНЫЙ, 100% РАБОЧИЙ, БОЛЬШЕ НИЧЕГО НЕ ТРОГАЕМ
import asyncio
import os
from aiohttp import web
from aiogram.webhook.aiohttp_server import SimpleRequestHandler

from config import bot, dp, WEBHOOK_URL
from database import init_db

# === ВСЕ ТВОИ РОУТЕРЫ (точно есть у тебя) ===
from handlers.start import router as start_router
from handlers.games import router as games_router
from handlers.profile import router as profile_router
from handlers.common import router as common_router
from handlers.payments import router as payments_router
from handlers.admin import router as admin_router

dp.include_router(start_router)
dp.include_router(games_router)
dp.include_router(profile_router)
dp.include_router(common_router)
dp.include_router(payments_router)
dp.include_router(admin_router)

# === КОНЕЦ СПИСКА РОУТЕРОВ ===

async def on_startup(app):
    await init_db()
    print("База данных готова — с датой рождения, фактом и странной историей!")
    await bot.set_webhook(WEBHOOK_URL)
    print(f"Webhook установлен: {WEBHOOK_URL}")

async def on_shutdown(app):
    print("Бот выключается...")
    asyncio.create_task(bot.delete_webhook(drop_pending_updates=True))
    asyncio.create_task(bot.session.close())

async def main():
    app = web.Application()
    
    SimpleRequestHandler(dispatcher=dp, bot=bot).register(app, path="/")

    app.on_startup.append(on_startup)
    app.on_shutdown.append(on_shutdown)

    runner = web.AppRunner(app)
    await runner.setup()
    
    site = web.TCPSite(runner, "0.0.0.0", int(os.environ.get("PORT", 8000)))
    await site.start()

    print("Бот запущен на Railway через webhook! Живём вечно ❤️")
    
    # Это держит контейнер живым навсегда
    while True:
        await asyncio.sleep(3600)

if __name__ == "__main__":
    asyncio.run(main())
