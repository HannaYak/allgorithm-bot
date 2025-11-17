# handlers/admin.py — ФИНАЛЬНАЯ ВЕРСИЯ 2025
from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.filters import Command
from config import ADMIN_ID, bot
import aiosqlite
import datetime
import asyncio

router = Router()

class AdminStates(StatesGroup):
    broadcast = State()
    support_reply = State()
    edit_rules = State()
    edit_price = State()
    edit_dates = State()

# ==================== ГЛАВНАЯ АДМИН-ПАНЕЛЬ ====================
@router.message(Command("admin"))
async def admin_main(message: types.Message):
    if message.from_user.id != ADMIN_ID:
        return await message.answer("⛔ Доступ запрещён")
    
    kb = [
        [types.InlineKeyboardButton(text="Игры и даты", callback_data="admin_games")],
        [types.InlineKeyboardButton(text="Активная игра", callback_data="admin_active")],
        [types.InlineKeyboardButton(text="Рассылка", callback_data="admin_broadcast")],
        [types.InlineKeyboardButton(text="Поддержка (чаты)", callback_data="admin_support")],
        [types.InlineKeyboardButton(text="Статистика", callback_data="admin_stats")],
    ]
    await message.answer("🔥 Админ-панель", reply_markup=types.InlineKeyboardMarkup(inline_keyboard=kb))

# ==================== СПИСОК ИГР ====================
@router.callback_query(F.data == "admin_games")
async def list_games(callback: types.CallbackQuery):
    async with aiosqlite.connect("bot.db") as db:
        db.row_factory = aiosqlite.Row
        async with db.execute("SELECT key, name, price, active FROM games") as cur:
            rows = await cur.fetchall()
    
    kb = []
    for r in rows:
        status = "🔥 Активна" if r["active"] else "⏳"
        kb.append([types.InlineKeyboardButton(
            text=f"{status} {r['name']} — {r['price']} PLN",
            callback_data=f"admin_game:{r['key']}"
        )])
    kb.append([types.InlineKeyboardButton(text="Назад", callback_data="admin_main")])
    
    await callback.message.edit_text("Выбери игру для редактирования:", reply_markup=types.InlineKeyboardMarkup(inline_keyboard=kb))

# ==================== РЕДАКТИРОВАНИЕ ИГРЫ ====================
@router.callback_query(lambda c: c.data.startswith("admin_game:"))
async def edit_game(callback: types.CallbackQuery, state: FSMContext):
    key = callback.data.split(":")[1]
    await state.update_data(game_key=key)
    
    async with aiosqlite.connect("bot.db") as db:
        db.row_factory = aiosqlite.Row
        async with db.execute("SELECT * FROM games WHERE key=?", (key,)) as cur:
            game = await cur.fetchone()
    
    kb = [
        [types.InlineKeyboardButton(text="Правила", callback_data="admin_rules")],
        [types.InlineKeyboardButton(text="Цена", callback_data="admin_price")],
        [types.InlineKeyboardButton(text="Даты и время", callback_data="admin_dates")],
        [types.InlineKeyboardButton(text="Активировать" if not game["active"] else "Деактивировать", 
                                   callback_data=f"admin_toggle:{key}")],
        [types.InlineKeyboardButton(text="Назад", callback_data="admin_games")],
    ]
    await callback.message.edit_text(
        f"*{game['name']}*\n\nПравила:\n{game['rules'][:500]}...\n\nЦена: {game['price']} PLN",
        reply_markup=types.InlineKeyboardMarkup(inline_keyboard=kb),
        parse_mode="Markdown"
    )

# ==================== ПРАВИЛА ====================
@router.callback_query(F.data == "admin_rules")
async def change_rules(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_text("Пришли новые правила:")
    await state.set_state(AdminStates.edit_rules)

@router.message(AdminStates.edit_rules)
async def save_rules(message: types.Message, state: FSMContext):
    data = await state.get_data()
    async with aiosqlite.connect("bot.db") as db:
        await db.execute("UPDATE games SET rules = ? WHERE key = ?", (message.text, data["game_key"]))
        await db.commit()
    await message.answer("Правила сохранены")
    await state.clear()

# ==================== ЦЕНА ====================
@router.callback_query(F.data == "admin_price")
async def change_price(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_text("Новая цена (PLN):")
    await state.set_state(AdminStates.edit_price)

@router.message(AdminStates.edit_price)
async def save_price(message: types.Message, state: FSMContext):
    if not message.text.isdigit():
        return await message.answer("Только число!")
    data = await state.get_data()
    async with aiosqlite.connect("bot.db") as db:
        await db.execute("UPDATE games SET price = ? WHERE key = ?", (int(message.text), data["game_key"]))
        await db.commit()
    await message.answer("Цена обновлена")
    await state.clear()

# ==================== АКТИВАЦИЯ ====================
@router.callback_query(lambda c: c.data.startswith("admin_toggle:"))
async def toggle_active(callback: types.CallbackQuery):
    key = callback.data.split(":")[1]
    async with aiosqlite.connect("bot.db") as db:
        await db.execute("UPDATE games SET active = 0")  # сбрасываем все
        await db.execute("UPDATE games SET active = 1 WHERE key = ?", (key,))
        await db.commit()
    await callback.answer("Активная игра изменена")
    await list_games(callback)

# ==================== РАССЫЛКА ====================
@router.callback_query(F.data == "admin_broadcast")
async def broadcast_start(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_text("Текст рассылки:")
    await state.set_state(AdminStates.broadcast)

@router.message(AdminStates.broadcast)
async def broadcast_send(message: types.Message, state: FSMContext):
    async with aiosqlite.connect("bot.db") as db:
        async with db.execute("SELECT user_id FROM users") as cur:
            users = [row[0] async for row in cur]
    sent = 0
    for uid in users:
        try:
            await bot.copy_message(uid, message.from_user.id, message.message_id)
            sent += 1
        except:
            pass
        await asyncio.sleep(0.04)
    await message.answer(f"Отправлено: {sent}")
    await state.clear()

# ==================== СТАТИСТИКА ====================
@router.callback_query(F.data == "admin_stats")
async def stats(callback: types.CallbackQuery):
    async with aiosqlite.connect("bot.db") as db:
        async with db.execute("SELECT COUNT(*) FROM users") as c: users = (await c.fetchone())[0]
        async with db.execute("SELECT COUNT(*) FROM payments WHERE status='completed'") as c: paid = (await c.fetchone())[0]
        async with db.execute("SELECT COALESCE(SUM(amount),0) FROM payments WHERE status='completed'") as c: revenue = (await c.fetchone())[0]
    await callback.message.edit_text(
        f"Статистика на {datetime.datetime.now().strftime('%d.%m.%Y %H:%M')}\n\n"
        f"Пользователей: {users}\n"
        f"Оплат: {paid}\n"
        f"Выручка: {revenue} PLN"
    )

# ==================== НАЗАД В ГЛАВНОЕ МЕНЮ ====================
@router.callback_query(F.data == "admin_main")
async def back(callback: types.CallbackQuery):
    await admin_main(callback.message)
