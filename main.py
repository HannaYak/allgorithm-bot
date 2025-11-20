# main.py — ФИНАЛЬНАЯ ВЕРСИЯ (РАБОТАЕТ НА 1000000%)
import asyncio
from config import bot, dp
from database import init_db
import os
from aiohttp import web
from aiogram.webhook.aiohttp_server import SimpleRequestHandler

from config import bot, dp, WEBHOOK_URL
from database import init_db

# Импортируем роутеры по правильным именам
from handlers import (
    start_router,
    games_router,
    profile_router,
    help_router,
    payments_router,
    admin_router,
    support_router
)

# Подключаем их
dp.include_router(start_router)
dp.include_router(games_router)
dp.include_router(profile_router)
dp.include_router(help_router)
dp.include_router(payments_router)
dp.include_router(admin_router)
dp.include_router(support_router)

sync def on_startup(app):
    await init_db()
    print("База данных готова — с датой рождения, фактом и странной историей!")

    if WEBHOOK_URL:
        await bot.set_webhook(url=WEBHOOK_URL)
        print(f"Webhook установлен: {WEBHOOK_URL}")
    else:
        print("WEBHOOK_URL не найден — запускаемся в polling (только локально)")


async def on_shutdown(app):
    print("Бот выключается...")
    await bot.delete_webhook(drop_pending_updates=True)
    await bot.session.close()


async def main():
    # Если локально — можно запустить polling (удобно для теста)
    if not WEBHOOK_URL or "railway.app" not in WEBHOOK_URL:
        print("Запуск в polling режиме (локально)")
        await init_db()
        await dp.start_polling(bot)

    else:
        # === РЕЖИМ RAILWAY — WEBHOOK ===
        app = web.Application()
        SimpleRequestHandler(dispatcher=dp, bot=bot).register(app, path="/")

        app.on_startup.append(on_startup)
        app.on_shutdown.append(on_shutdown)

        runner = web.AppRunner(app)
        await runner.setup()
        site = web.TCPSite(runner, "0.0.0.0", int(os.environ.get("PORT", 8000)))
        await site.start()

        print("Бот запущен на Railway через webhook! Живём вечно")
        await asyncio.Event().wait()  # держим контейнер живым


if __name__ == "__main__":
    asyncio.run(main())
