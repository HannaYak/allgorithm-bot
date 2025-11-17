# handlers/games.py
from aiogram import Router, types, F
from database import db

router = Router()

GAMES = {
    "meet_eat": "Meet&Eat — 50 PLN",
    "lock_stock": "Лок Сток — 60 PLN",
    "bar_liar": "Бар Лжецов — 55 PLN",
    "speed_dating": "Быстрые Свидания — 70 PLN"
}

@router.callback_query(F.data == "show_games")
async def show_games(callback: types.CallbackQuery):
    async with aiosqlite.connect("bot.db") as conn:
        conn.row_factory = aiosqlite.Row
        async with conn.execute("SELECT key, name, price, rules FROM games") as cur:
            rows = await cur.fetchall()
    
    keyboard = []
    for row in rows:
        key = row["key"]
        keyboard.append([
            types.InlineKeyboardButton(text=f"{row['name']} — {row['price']} PLN", callback_data=f"game_rules:{key}"),
        ])
    keyboard.append([types.InlineKeyboardButton(text="Назад", callback_data="back_to_start")])
    
    await callback.message.edit_text(
        "Выбери игру и посмотри правила:",
        reply_markup=types.InlineKeyboardMarkup(inline_keyboard=keyboard)
    )

@router.callback_query(lambda c: c.data.startswith("game_rules:"))
async def show_game_rules(callback: types.CallbackQuery):
    key = callback.data.split(":")[1]
    async with aiosqlite.connect("bot.db") as conn:
        conn.row_factory = aiosqlite.Row
        async with conn.execute("SELECT name, price, rules FROM games WHERE key=?", (key,)) as cur:
            game = await cur.fetchone()
    
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text="Оплатить", callback_data=f"pay:{key}")],
        [types.InlineKeyboardButton(text="Другие игры", callback_data="show_games")],
        [types.InlineKeyboardButton(text="Назад в меню", callback_data="back_to_start")]
    ])
    
    await callback.message.edit_text(
        f"*{game['name']}*\n\n{game['rules']}\n\nЦена: {game['price']} PLN",
        reply_markup=keyboard,
        parse_mode="Markdown"
    )
