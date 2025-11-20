# handlers/games.py — ФИНАЛЬНАЯ ВЕРСИЯ, БЕЗ ОШИБОК
from aiogram import Router, types, F
import aiosqlite
from datetime import datetime, timedelta

router = Router()

@router.message(F.text == "Игры")
async def show_events(message: types.Message):
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
        await message.answer("На ближайшие 2 недели мест нет 😔\n\nСкоро добавлю новые события!")
        return

    kb = []
    for e in events:
        places = e["seats_total"] - e["seats_taken"]
        date_str = e["datetime"][:16].replace("T", " ")
        kb.append([types.InlineKeyboardButton(
            text=f"{e['name']} — {date_str} — {places} мест",
            callback_data=f"event:{e['id']}"
        )])

    await message.answer(
        "Ближайшие игры (2 недели):",
        reply_markup=types.InlineKeyboardMarkup(inline_keyboard=kb)
    )

@router.callback_query(lambda c: c.data and c.data.startswith("event:"))
async def show_event_details(callback: types.CallbackQuery):
    event_id = int(callback.data.split(":")[1])
    
    async with aiosqlite.connect("bot.db") as db:
        db.row_factory = aiosqlite.Row
        async with db.execute("SELECT * FROM events WHERE id = ?", (event_id,)) as cur:
            event = await cur.fetchone()

    if not event or event["seats_taken"] >= event["seats_total"]:
        await callback.answer("Мест уже нет!", show_alert=True)
        return

    places = event["seats_total"] - event["seats_taken"]
    date_str = event["datetime"][:16].replace("T", " ")

    kb = [
        [types.InlineKeyboardButton(text=f"Записаться — {event['price']} zł", callback_data=f"pay:{event['id']}")],
        [types.InlineKeyboardButton(text="⬅ Назад", callback_data="back_to_events")]
    ]

    await callback.message.edit_text(
        f"*{event['name']}*\n\n"
        f"📅 Дата и время: {date_str}\n"
        f"📍 Адрес: {event['address']}\n"
        f"🎟 Осталось мест: {places}\n"
        f"💰 Цена: {event['price']} zł\n\n"
        f"После оплаты ты в списке и получишь все детали!",
        reply_markup=types.InlineKeyboardMarkup(inline_keyboard=kb),
        parse_mode="Markdown"
    )

@router.callback_query(F.data == "back_to_events")
async def back_to_events(callback: types.CallbackQuery):
    await show_events(callback.message)
