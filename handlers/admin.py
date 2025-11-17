# handlers/admin_full.py
from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.filters import Command
from config import ADMIN_ID, bot
import aiosqlite
import datetime

router = Router()

# === Состояния админа ===
class AdminStates(StatesGroup):
    waiting_broadcast = State()
    waiting_support_reply = State()
    waiting_game_rules = State()
    waiting_game_price = State()

# === Главная админ-панель ===
@router.message(Command("admin"))
async def admin_panel(message: types.Message):
    if message.from_user.id != ADMIN_ID:
        return await message.answer("⛔ Доступ запрещён")
    
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text="Игры", callback_data="admin_games_list")],
        [types.InlineKeyboardButton(text="Активная игра", callback_data="admin_active_game")],
        [types.InlineKeyboardButton(text="Рассылка", callback_data="admin_broadcast")],
        [types.InlineKeyboardButton(text="Поддержка", callback_data="admin_support")],
        [types.InlineKeyboardButton(text="Статистика", callback_data="admin_stats")],
    ])
    await message.answer("Админ-панель", reply_markup=keyboard)

# === Список игр (редактирование) ===
@router.callback_query(F.data == "admin_games_list")
async def admin_games_list(callback: types.CallbackQuery):
    async with aiosqlite.connect("bot.db") as db:
        db.row_factory = aiosqlite.Row
        async with db.execute("SELECT key, name, price, active FROM games") as cur:
            games = await cur.fetchall()
    
    keyboard = []
    for game in games:
        status = "Активна" if game["active"] else "Неактивна"
        keyboard.append([types.InlineKeyboardButton(
            text=f"{game['name']} — {game['price']} PLN [{status}]",
            callback_data=f"admin_edit_game:{game['key']}"
        )])
    keyboard.append([types.InlineKeyboardButton(text="Назад", callback_data="admin_back")])
    
    await callback.message.edit_text("Редактирование игр:", reply_markup=types.InlineKeyboardMarkup(inline_keyboard=keyboard))

# === Редактирование конкретной игры ===
@router.callback_query(lambda c: c.data.startswith("admin_edit_game:"))
async def admin_edit_game(callback: types.CallbackQuery, state: FSMContext):
    key = callback.data.split(":")[1]
    await state.update_data(edit_game=key)
    
    async with aiosqlite.connect("bot.db") as db:
        db.row_factory = aiosqlite.Row
        async with db.execute("SELECT * FROM games WHERE key=?", (key,)) as cur:
            game = await cur.fetchone()
    
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text="Изменить правила", callback_data="admin_change_rules")],
        [types.InlineKeyboardButton(text="Изменить цену", callback_data="admin_change_price")],
        [types.InlineKeyboardButton(text="Активировать игру" if not game["active"] else "Деактивировать", 
                                  callback_data=f"admin_toggle_active:{key}")],
        [types.InlineKeyboardButton(text="Назад", callback_data="admin_games_list")],
    ])
    
    await callback.message.edit_text(
        f"Редактирование: *{game['name']}*\n\nТекущие правила:\n{game['rules']}\n\nЦена: {game['price']} PLN",
        reply_markup=keyboard, parse_mode="Markdown"
    )

# === Смена правил ===
@router.callback_query(F.data == "admin_change_rules")
async def admin_change_rules(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_text("Пришли новые правила игры:")
    await state.set_state(AdminStates.waiting_game_rules)

@router.message(AdminStates.waiting_game_rules)
async def save_new_rules(message: types.Message, state: FSMContext):
    data = await state.get_data()
    key = data["edit_game"]
    async with aiosqlite.connect("bot.db") as db:
        await db.execute("UPDATE games SET rules = ? WHERE key = ?", (message.text, key))
        await db.commit()
    await message.answer("Правила обновлены!")
    await state.clear()
    await admin_edit_game(message, state)  # возвращаем в редактирование

# === Смена цены ===
@router.callback_query(F.data == "admin_change_price")
async def admin_change_price(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_text("Пришли новую цену (только число):")
    await state.set_state(AdminStates.waiting_game_price)

@router.message(AdminStates.waiting_game_price)
async def save_new_price(message: types.Message, state: FSMContext):
    if not message.text.isdigit():
        return await message.answer("Нужно число!")
    data = await state.get_data()
    key = data["edit_game"]
    async with aiosqlite.connect("bot.db") as db:
        await db.execute("UPDATE games SET price = ? WHERE key = ?", (int(message.text), key))
        await db.commit()
    await message.answer("Цена обновлена!")
    await state.clear()

# === Активация/деактивация ===
@router.callback_query(lambda c: c.data.startswith("admin_toggle_active:"))
async def toggle_active(callback: types.CallbackQuery):
    key = callback.data.split(":")[1]
    async with aiosqlite.connect("bot.db") as db:
        await db.execute("UPDATE games SET active = NOT active WHERE key = ?", (key,))
        await db.commit()
    await callback.answer("Статус изменён")
    await admin_games_list(callback)

# === Показать текущую активную игру ===
@router.callback_query(F.data == "admin_active_game")
async def show_active_game(callback: types.CallbackQuery):
    async with aiosqlite.connect("bot.db") as db:
        db.row_factory = aiosqlite.Row
        async with db.execute("SELECT name FROM games WHERE active = 1") as cur:
            game = await cur.fetchone()
    text = f"Активная игра: {game['name'] if game else 'нет'}"
    await callback.message.edit_text(text, reply_markup=types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text="Назад", callback_data="admin_back")]
    ]))

# === Рассылка ===
@router.callback_query(F.data == "admin_broadcast")
async def start_broadcast(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_text("Пришли текст рассылки:")
    await state.set_state(AdminStates.waiting_broadcast)

@router.message(AdminStates.waiting_broadcast)
async def send_broadcast(message: types.Message, state: FSMContext):
    async with aiosqlite.connect("bot.db") as db:
        async with db.execute("SELECT user_id FROM users") as cur:
            users = await cur.fetchall()
    
    sent = 0
    for user in users:
        try:
            await bot.send_message(user[0], message.text)
            sent += 1
        except:
            pass
        await asyncio.sleep(0.04)  # антифлуд
    
    await message.answer(f"Рассылка отправлена {sent} пользователям")
    await state.clear()

# === Поддержка (ответы в чат) ===
@router.callback_query(F.data == "admin_support")
async def support_list(callback: types.CallbackQuery):
    # Пока просто покажем, что работает
    await callback.message.edit_text("Поддержка включена — все сообщения от пользователей приходят сюда (в будущем будет полноценный чат)")

# === Статистика ===
@router.callback_query(F.data == "admin_stats")
async def admin_stats(callback: types.CallbackQuery):
    async with aiosqlite.connect("bot.db") as db:
        async with db.execute("SELECT COUNT(*) FROM users") as c: users = (await c.fetchone())[0]
        async with db.execute("SELECT COUNT(*) FROM payments WHERE status='completed'") as c: payments = (await c.fetchone())[0]
        async with db.execute("SELECT SUM(amount) FROM payments WHERE status='completed'") as c: revenue = (await c.fetchone())[0] or 0
    await callback.message.edit_text(
        f"Статистика\n\n"
        f"Пользователей: {users}\n"
        f"Оплат: {payments}\n"
        f"Выручка: {revenue} PLN"
    )

# === Назад в админку ===
@router.callback_query(F.data == "admin_back")
async def back_to_admin(callback: types.CallbackQuery):
    await admin_panel(callback.message)
