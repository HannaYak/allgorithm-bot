# database.py — ФИНАЛЬНАЯ ВЕРСИЯ (без объекта db)
import aiosqlite
import datetime
from typing import Optional, Dict

DB_NAME = "bot.db"

async def init_db():
    async with aiosqlite.connect(DB_NAME) as conn:
        await conn.executescript("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                name TEXT,
                age INTEGER,
                games_played INTEGER DEFAULT 0,
                loyalty INTEGER DEFAULT 0,
                created_at TEXT
            );
            CREATE TABLE IF NOT EXISTS payments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                payment_id TEXT UNIQUE,
                game TEXT,
                amount INTEGER,
                status TEXT DEFAULT 'pending',
                created_at TEXT
            );
            CREATE TABLE IF NOT EXISTS games (
                key TEXT PRIMARY KEY,
                name TEXT,
                price INTEGER,
                rules TEXT,
                active INTEGER DEFAULT 0
            );
        """)
        await conn.executemany("""
            INSERT OR IGNORE INTO games (key, name, price, rules) VALUES (?, ?, ?, ?)
        """, [
            ("meet_eat", "Meet&Eat", 50, "Правила Meet&Eat…"),
            ("lock_stock", "Лок Сток", 60, "Правила Лок Сток…"),
            ("bar_liar", "Бар Лжецов", 55, "Правила Бар Лжецов…"),
            ("speed_dating", "Быстрые Свидания", 70, "Правила Свиданий…")
        ])
        await conn.commit()
    print("База данных готова")

# === ВСЕ ФУНКЦИИ ===
async def get_user(user_id: int) -> Optional[Dict]:
    async with aiosqlite.connect(DB_NAME) as conn:
        conn.row_factory = aiosqlite.Row
        async with conn.execute("SELECT * FROM users WHERE user_id = ?", (user_id,)) as cur:
            row = await cur.fetchone()
            return dict(row) if row else None

async def add_user(user_id: int, name: str = None, age: int = None):
    async with aiosqlite.connect(DB_NAME) as conn:
        await conn.execute(
            "INSERT OR REPLACE INTO users (user_id, name, age, created_at) VALUES (?, ?, ?, ?)",
            (user_id, name, age, datetime.datetime.now().isoformat())
        )
        await conn.commit()

async def get_stats() -> Dict:
    async with aiosqlite.connect(DB_NAME) as conn:
        async with conn.execute("SELECT COUNT(*) FROM users") as c:
            users = (await c.fetchone())[0]
        async with conn.execute("SELECT COUNT(*) FROM payments WHERE status='completed'") as c:
            payments = (await c.fetchone())[0]
        async with conn.execute("SELECT COALESCE(SUM(amount),0) FROM payments WHERE status='completed'") as c:
            revenue = (await c.fetchone())[0]
        async with conn.execute("SELECT COALESCE(SUM(games_played),0) FROM users") as c:
            games = (await c.fetchone())[0]
        return {"users": users, "payments": payments, "revenue": revenue, "games": games}

# Добавь сюда остальные функции (add_payment, update_payment_status и т.д.) — если их нет, скажи, я пришлю
