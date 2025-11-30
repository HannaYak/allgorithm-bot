import aiosqlite

DB = "bot.db"

async def init():
    async with aiosqlite.connect(DB) as db:
        await db.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                name TEXT, birth TEXT, fact TEXT, story TEXT,
                visits INTEGER DEFAULT 0,
                free_game INTEGER DEFAULT 0
            )
        ''')
        await db.execute('''
            CREATE TABLE IF NOT EXISTS events (
                id TEXT PRIMARY KEY,
                game TEXT, datetime TEXT, kitchen TEXT, location TEXT,
                max_places INTEGER, taken INTEGER DEFAULT 0, price INTEGER
            )
        ''')
        await db.execute('''
            CREATE TABLE IF NOT EXISTS bookings (
                user_id INTEGER, event_id TEXT,
                PRIMARY KEY (user_id, event_id)
            )
        ''')
        await db.commit()
