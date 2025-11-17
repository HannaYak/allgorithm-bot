# handlers/admin.py — ПОЛНАЯ РАБОЧАЯ АДМИНКА
from aiogram import Router, types, F
from aiogram.filters import Command
import aiosqlite

router = Router()
ADMIN_ID = 5179631743  # ← твой основной ID

@router.message(Command("admin"))
async def admin_panel(message: types.Message):
    if message.from_user.id != ADMIN_ID:
        return
    kb = [
        [types.InlineKeyboardButton(text="Создать событие", callback_data="admin_create_event")],
        [types.InlineKeyboardButton(text="Все события", callback_data="admin_events_list")],
        [types.InlineKeyboardButton(text="Статистика", callback_data="admin_stats")],
        [types.InlineKeyboardButton(text="Поддержка (входящие)", callback_data="admin_support")],
    ]
    await message.answer("Админ-панель 🔥", reply_markup=types.InlineKeyboardMarkup(inline_keyboard=kb))

@router.callback_query(F.data == "admin_support")
async def support_info(callback: types.CallbackQuery):
    await callback.message.edit_text("Поддержка работает!\n\nВсе вопросы игроков приходят тебе в личку мгновенно.\nОтвечай реплаем — и ответ уйдёт игроку.")

@router.callback_query(F.data == "admin_stats")
async def stats(callback: types.CallbackQuery):
    async with aiosqlite.connect("bot.db") as db:
        async with db.execute("SELECT COUNT(*) FROM users") as cur:
            users = (await cur.fetchone())[0]
        async with db.execute("SELECT COUNT(*) FROM events") as cur:
            events = (await cur.fetchone())[0]
        async with db.execute("SELECT COUNT(*) FROM payments WHERE status='completed'") as cur:
            paid = (await cur.fetchone())[0]
    await callback.message.edit_text(
        f"Статистика бота:\n\n"
        f"Пользователей: {users}\n"
        f"Создано событий: {events}\n"
        f"Оплачено записей: {paid}\n\n"
        f"Ты — королева Варшавы ❤️"
    )

@router.callback_query(F.data == "admin_events_list")
async def list_events(callback: types.CallbackQuery):
    async with aiosqlite.connect("bot.db") as db:
        db.row_factory = aiosqlite.Row
        async with db.execute("SELECT id, name, datetime, seats_taken, seats_total FROM events ORDER BY datetime") as cur:
            events = await cur.fetchall()
    
    if not events:
        await callback.message.edit_text("Пока нет событий. Создай первое!")
        return
    
    text = "Все события:\n\n"
    for e in events:
        text += f"{e['name']}\n{e['datetime'][:16].replace('T',' ')} — {e['seats_taken']}/{e['seats_total']} мест\n\n"
    await callback.message.edit_text(text)
