# database.py — ФИНАЛЬНАЯ РАБОЧАЯ ВЕРСИЯ
import aiosqlite
import datetime

DB_NAME = "bot.db"

# ←←← ВСЁ ВНУТРИ ФУНКЦИИ! ←←←
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
                game_key TEXT,
                amount INTEGER,
                status TEXT DEFAULT 'pending',
                created_at TEXT
            );
            
            CREATE TABLE IF NOT EXISTS games (
                key TEXT PRIMARY KEY,
                name TEXT,
                price INTEGER,
                rules TEXT,
                seats_total INTEGER DEFAULT 20,
                seats_taken INTEGER DEFAULT 0
            );
        """)
        
        # Добавляем игры, если их ещё нет
        await conn.executemany("""
            INSERT OR IGNORE INTO games (key, name, price, rules, seats_total, seats_taken) 
            VALUES (?, ?, ?, ?, ?, 0)
        """, [
            ("meet_eat", "Meet&Eat", 50, "Правила Meet&Eat…", 20),
            ("lock_stock", "Лок Сток", 60, "Правила Лок Сток…", 16),
            ("bar_liar", "Бар Лжецов", 55, "Правила Бар Лжецов…", 24),
            ("speed_dating", "Быстрые Свидания", 70, "Правила Свиданий…", 18),
        ])
        
        await conn.commit()
    print("База данных готова и обновлена!")

# Остальные функции (по мере надобности добавишь)
async def get_user(user_id: int):
    async with aiosqlite.connect(DB_NAME) as conn:
        conn.row_factory = aiosqlite.Row
        async with conn.execute("SELECT * FROM users WHERE user_id = ?", (user_id,)) as cur:
            row = await cur.fetchone()
            return dict(row) if row else None

async def add_user(user_id: int, name: str = None, age: int = None):
    async with aiosqlite.connect(DB_NAME) as conn:
        await conn.execute("""
            INSERT OR REPLACE INTO users (user_id, name, age, created_at) 
            VALUES (?, ?, ?, ?)
        """, (user_id, name, age, datetime.datetime.now().isoformat()))
        await conn.commit()
