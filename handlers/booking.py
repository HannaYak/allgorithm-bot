from aiogram import Router, types
from database import get_user
import aiosqlite

router = Router()

# Показываем доступные даты для выбранного мероприятия
@router.callback_query(lambda c: c.data.startswith("event_"))
async def show_available_dates(callback: types.CallbackQuery):
    user = await get_user(callback.from_user.id)
    if not user: return

    event_type = callback.data.split("_")[1]
    type_names = {
        "eatmeet": "Eat & Meet / Talk & Toast",
        "auction": "Аукцион странных историй историй",
        "stock": "Stock & Know",
        "speed": "Быстрые свидания"
    }

    async with aiosqlite.connect("bot.db") as db:
        async with db.execute("""
            SELECT id, datetime, place, price FROM events 
            WHERE type = ? AND datetime > datetime('now')
            ORDER BY datetime
        """, (event_type,)) as cur:
            events = await cur.fetchall()

    if not events:
        await callback.message.edit_text("Нет доступных дат. Скоро добавим!")
        return

    kb = []
    for ev in events[:10]:  # показываем ближайшие 10
        kb.append([types.InlineKeyboardButton(
            text=f"{ev[1]} — {ev[3]} PLN",
            callback_data=f"select_{ev[0]}"
        )])
    kb.append([types.InlineKeyboardButton(text="Назад", callback_data="events")])

    await callback.message.edit_text(
        f"Доступные даты для {type_names.get(event_type)}:",
        reply_markup=types.InlineKeyboardMarkup(inline_keyboard=kb)
    )

# Выбор даты → оплата
@router.callback_query(lambda c: c.data.startswith("select_"))
async def select_date(callback: types.CallbackQuery):
    event_id = int(callback.data.split("_")[1])
    
    # Здесь вызываем твой payments.py
    await callback.message.edit_text(
        "Переход к оплате...\n\n"
        "Нажми кнопку ниже:",
        reply_markup=types.InlineKeyboardMarkup(inline_keyboard=[
            [types.InlineKeyboardButton(text="Оплатить сейчас", callback_data=f"pay_event_{event_id}")],
            [types.InlineKeyboardButton(text="Отмена", callback_data="events")]
        ])
    )
