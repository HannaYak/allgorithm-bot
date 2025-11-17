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
            CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        name TEXT,
        birthdate TEXT,        -- новая
        age INTEGER,
        fun_fact TEXT,         -- новая
        crazy_story TEXT,      -- новая
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


async def add_user(user_id: int, name: str = None, age: int = None):
    async with aiosqlite.connect(DB_NAME) as conn:
        await conn.execute("""
            INSERT OR REPLACE INTO users (user_id, name, age, created_at) 
            VALUES (?, ?, ?, ?)
        """, (user_id, name, age, datetime.datetime.now().isoformat()))
        await conn.commit()

async def get_user(user_id: int):
    async with aiosqlite.connect(DB_NAME) as conn:
        conn.row_factory = aiosqlite.Row
        async with conn.execute("SELECT * FROM users WHERE user_id = ?", (user_id,)) as cur:
            row = await cur.fetchone()
            return dict(row) if row else None

async def add_user(user_id: int, name: str = None, birthdate: str = None, age: int = 0,
                  fun_fact: str = None, crazy_story: str = None):
    async with aiosqlite.connect(DB_NAME) as conn:
        await conn.execute("""
            INSERT OR REPLACE INTO users 
            (user_id, name, birthdate, age, fun_fact, crazy_story, created_at) 
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (user_id, name, birthdate, age, fun_fact, crazy_story, datetime.now().isoformat()))
        await conn.commit()
