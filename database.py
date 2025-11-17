# database.py — только актуальная версия с events
import aiosqlite
import datetime

DB_NAME = "bot.db"

async def init_db():
    async with aiosqlite.connect(DB_NAME) as conn:
        # Удаляем старые таблицы, если они были (один раз)
        await conn.execute("DROP TABLE IF EXISTS games")
        await conn.execute("DROP TABLE IF EXISTS payments")  # если хочешь с нуля
        
        # Создаём только нужные таблицы
        await conn.executescript("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                name TEXT,
                age INTEGER,
                games_played INTEGER DEFAULT 0,
                loyalty INTEGER DEFAULT 0,
                created_at TEXT
            );

            CREATE TABLE IF NOT EXISTS events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                game_type TEXT,
                name TEXT,
                datetime TEXT,
                address TEXT,
                price INTEGER,
                seats_total INTEGER DEFAULT 20,
                seats_taken INTEGER DEFAULT 0
            );

            CREATE TABLE IF NOT EXISTS payments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                event_id INTEGER,
                amount INTEGER,
                status TEXT DEFAULT 'completed',
                created_at TEXT
            );
        """)
        await conn.commit()
    print("База данных готова — только с events!")
