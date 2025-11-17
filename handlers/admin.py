# handlers/admin.py — ФИНАЛЬНАЯ АДМИНКА 2025 (поддержка + активные игры)
from aiogram import Router, types, F
from aiogram.filters import Command
from config import ADMIN_ID
import aiosqlite

router = Router()

@router.message(Command("admin"))
async def admin_panel(message: types.Message):
    if message.from_user.id != ADMIN_ID:
        return
    
    kb = [
        [types.InlineKeyboardButton(text="Игры и активность", callback_data="admin_games")],
        [types.InlineKeyboardButton(text="Поддержка (чаты)", callback_data="admin_support")],
        [types.InlineKeyboardButton(text="Статистика", callback_data="admin_stats")],
    ]
    await message.answer("Админ-панель", reply_markup=types.InlineKeyboardMarkup(inline_keyboard=kb))

# Список игр + переключение активности
@router.callback_query(F.data == "admin_games")
async def admin_games_list(callback: types.CallbackQuery):
    async with aiosqlite.connect("bot.db") as db:
        db.row_factory = aiosqlite.Row
        async with db.execute("SELECT key, name, price, active FROM games") as cur:
            games = await cur.fetchall()
    
    kb = []
    for g in games:
        status = "Активна 🔥" if g["active"] else "Неактивна"
        kb.append([types.InlineKeyboardButton(
            text=f"{status} {g['name']} — {g['price']} PLN",
            callback_data=f"toggle_active:{g['key']}"
        )])
    kb.append([types.InlineKeyboardButton(text="Обновить", callback_data="admin_games")])
    
    await callback.message.edit_text(
        "Нажми на игру — она станет активной (все остальные отключатся):",
        reply_markup=types.InlineKeyboardMarkup(inline_keyboard=kb)
    )

# Переключение активности
@router.callback_query(lambda c: c.data.startswith("toggle_active:"))
async def toggle_game_active(callback: types.CallbackQuery):
    key = callback.data.split(":")[1]
    async with aiosqlite.connect("bot.db") as db:
        await db.execute("UPDATE games SET active = 0")  # сбрасываем все
        await db.execute("UPDATE games SET active = 1 WHERE key = ?", (key,))
        await db.commit()
    await callback.answer(f"Игра {key} теперь активна!")
    await admin_games_list(callback)

# Поддержка — все неотвеченные сообщения приходят админу
@router.callback_query(F.data == "admin_support")
async def admin_support(callback: types.CallbackQuery):
    await callback.message.edit_text(
        "Поддержка работает так:\n\n"
        "Любой игрок пишет в бота → сообщение сразу приходит тебе\n"
        "Ты отвечаешь реплаем на это сообщение → ответ уходит игроку\n\n"
        "Всё уже работает! Просто жди первых вопросов ❤️"
    )

# Статистика
@router.callback_query(F.data == "admin_stats")
async def admin_stats(callback: types.CallbackQuery):
    async with aiosqlite.connect("bot.db") as db:
        async with db.execute("SELECT COUNT(*) FROM users") as c: users = (await c.fetchone())[0]
        async with db.execute("SELECT COUNT(*) FROM payments WHERE status='completed'") as c: paid = (await c.fetchone())[0]
        async with db.execute("SELECT COALESCE(SUM(amount),0) FROM payments WHERE status='completed'") as c: revenue = (await c.fetchone())[0]
        async with db.execute("SELECT name FROM games WHERE active = 1") as c:
            active_game = await c.fetchone()
            active_name = active_game["name"] if active_game else "нет"
    await callback.message.edit_text(
        f"Статистика\n\n"
        f"Пользователей: {users}\n"
        f"Оплат: {paid}\n"
        f"Выручка: {revenue} PLN\n"
        f"Активная игра: {active_name}"
    )

@router.callback_query(F.data == "admin_events")
async def admin_create_event(callback: types.CallbackQuery):
    kb = [
        [types.InlineKeyboardButton("Meet&Eat", callback_data="new_meet_eat")],
        [types.InlineKeyboardButton("Лок Сток", callback_data="new_lock_stock")],
        [types.InlineKeyboardButton("Бар Лжецов", callback_data="new_bar_liar")],
        [types.InlineKeyboardButton("Свидания", callback_data="new_speed_dating")],
    ]
    await callback.message.edit_text("Выбери игру для нового события:", reply_markup=types.InlineKeyboardMarkup(inline_keyboard=kb))
