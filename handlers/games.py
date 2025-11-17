# handlers/games.py — ВСЕ ИГРЫ СВОБОДНЫ, МЕСТА ОТСЛЕЖИВАЮТСЯ
from aiogram import Router, types, F
import aiosqlite

router = Router()

@router.message(F.text == "Игры")
async def show_games(message: types.Message):
    async with aiosqlite.connect("bot.db") as db:
        db.row_factory = aiosqlite.Row
        async with db.execute("""
            SELECT name, price, seats_total, seats_taken, key 
            FROM games 
            WHERE seats_taken < seats_total
            ORDER BY name
        """) as cur:
            games = await cur.fetchall()

    if not games:
        return await message.answer("На ближайшие игры мест нет 😔\nНо скоро будут новые!")

    kb = []
    for g in games:
        places = g["seats_total"] - g["seats_taken"]
        kb.append([types.InlineKeyboardButton(
            text=f"{g['name']} — {g['price']} PLN ({places} мест)",
            callback_data=f"game:{g['key']}"
        )])

    await message.answer("Выбери игру и запишись:", reply_markup=types.InlineKeyboardMarkup(inline_keyboard=kb))

# Показ правил + кнопка оплаты
@router.callback_query(lambda c: c.data.startswith("game:"))
async def show_game(callback: types.CallbackQuery):
    key = callback.data.split(":")[1]
    async with aiosqlite.connect("bot.db") as db:
        db.row_factory = aiosqlite.Row
        async with db.execute("SELECT * FROM games WHERE key=?", (key,)) as cur:
            game = await cur.fetchone()

    places = game["seats_total"] - game["seats_taken"]
    kb = [
        [types.InlineKeyboardButton(text=f"Записаться ({game['price']} PLN)", callback_data=f"pay:{key}")],
        [types.InlineKeyboardButton(text="Назад к играм", callback_data="back_games")]
    ]

    await callback.message.edit_text(
        f"*{game['name']}*\n\n"
        f"{game['rules']}\n\n"
        f"Осталось мест: {places}\n"
        f"Цена: {game['price']} PLN",
        reply_markup=types.InlineKeyboardMarkup(inline_keyboard=kb),
        parse_mode="Markdown"
    )

@router.callback_query(F.data == "back_games")
async def back(callback: types.CallbackQuery):
    await show_games(callback.message)
