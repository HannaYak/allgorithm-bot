# handlers/games.py — ФИНАЛЬНЫЙ И РАБОЧИЙ
from aiogram import Router, types, F
import aiosqlite

router = Router()

# Кнопка "Игры" из главного меню
@router.message(F.text == "Игры")
async def show_games_list(message: types.Message):
    async with aiosqlite.connect("bot.db") as db:
        db.row_factory = aiosqlite.Row
        async with db.execute("SELECT key, name, price FROM games") as cur:
            games = await cur.fetchall()

    if not games:
        return await message.answer("Игры пока не добавлены. Скоро будут!")

    kb = []
    for game in games:
        kb.append([types.InlineKeyboardButton(
            text=f"{game['name']} — {game['price']} PLN",
            callback_data=f"game_rules:{game['key']}"
        )])
    kb.append([types.InlineKeyboardButton(text="Назад в меню", callback_data="back_to_menu")])

    await message.answer(
        "Выбери игру и посмотри правила:",
        reply_markup=types.InlineKeyboardMarkup(inline_keyboard=kb)
    )

# Показ правил игры
@router.callback_query(lambda c: c.data.startswith("game_rules:"))
async def show_game_rules(callback: types.CallbackQuery):
    key = callback.data.split(":")[1]
    async with aiosqlite.connect("bot.db") as db:
        db.row_factory = aiosqlite.Row
        async with db.execute("SELECT name, rules, price FROM games WHERE key=?", (key,)) as cur:
            game = await cur.fetchone()

    kb = [
        [types.InlineKeyboardButton(text="Оплатить", callback_data=f"pay:{key}")],
        [types.InlineKeyboardButton(text="Другие игры", callback_data="show_games")],
        [types.InlineKeyboardButton(text="В меню", callback_data="back_to_menu")]
    ]

    await callback.message.edit_text(
        f"*{game['name']}*\n\n{game['rules']}\n\nЦена: {game['price']} PLN",
        reply_markup=types.InlineKeyboardMarkup(inline_keyboard=kb),
        parse_mode="Markdown"
    )

# Возврат в меню
@router.callback_query(F.data == "back_to_menu")
async def back_to_menu(callback: types.CallbackQuery):
    from handlers.start import main_menu_keyboard
    await callback.message.edit_text("Главное меню:", reply_markup=None)
    await callback.message.answer("Выбери:", reply_markup=main_menu_keyboard())
