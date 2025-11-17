# handlers/games.py — ТОЛЬКО ДЛЯ СОБЫТИЙ (events), БЕЗ games!
from aiogram import Router, types, F
import aiosqlite
from datetime import datetime, timedelta

router = Router()

@router.message(F.text == "Игры")
async def show_events(message: types.Message):
    # Показываем события на ближайшие 14 дней
    deadline = (datetime.now() + timedelta(days=14)).strftime("%Y-%m-%d %H:%M")

    async with aiosqlite.connect("bot.db") as db:
        db.row_factory = aiosqlite.Row
        async with db.execute("""
            SELECT id, name, datetime, address, price, seats_total, seats_taken 
            FROM events 
            WHERE datetime <= ? AND seats_taken < seats_total
            ORDER BY datetime
        """, (deadline,)) as cur:
            events = await cur.fetchall()

    if not events:
        await message.answer(
            "На ближайшие 2 недели мест нет 😔\n\n"
            "Но скоро будут новые события — следи за обновлениями!"
        )
        return

    kb = []
    for e in events:
        places_left = e["seats_total"] - e["seats_taken"]
        date_clean = e["datetime"][:16].replace("T", " ").replace("-", "‑")
        kb.append([types.InlineKeyboardButton(
            text=f"{e['name']} — {date_clean} — {places_left} мест",
            callback_data=f"event:{e['id']}"
        )])

    await message.answer(
        "Ближайшие игры (2 недели вперёд):",
        reply_markup=types.InlineKeyboardMarkup(inline_keyboard=kb)
    )

# Показ деталки события
@router.callback_query(lambda c: c.data and c.data.startswith("event:"))
async def show_event_details(callback: types.CallbackQuery):
    event_id = callback.data.split(":")[1]
    
    async with aiosqlite.connect("bot.db") as db:
        db.row_factory = aiosqlite.Row
        async with db.execute("SELECT * FROM events WHERE id = ?", (event_id,)) as cur:
            event = await cur.fetchone()

    if not event or event["seats_taken"] >= event["seats_total"]:
        await callback.answer("Мест уже нет!", show_alert=True)
        return

    places = event["seats_total"] - event["seats_taken"]
    kb = [
        [types.InlineKeyboardButton(text=f"Записаться — {event['price']} zł", callback_data=f"pay:{event['id']}")],
        [types.InlineKeyboardButton(text="⬅ Назад к списку", callback_data="back_to_events")]
    ]

    await callback.message.edit_text(
        f"*{event['name']}*\n\n"
        f"Дата и время: {event['datetime'][:16].replace('T', ' ')}\n"
        f"Адрес: {event['address']}\n"
        f"Осталось мест: {places}\n"
        f"Цена: {event['price']} zł\n\n"
        f"После оплаты — ты в списке и получишь все детали!",
        reply_markup=types.InlineKeyboardMarkup(inline_keyboard=kb),
        parse_mode
