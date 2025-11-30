from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
import aiosqlite

router = Router()

@router.message(F.text.in_(["Talk & Toast", "Stock & Know", "Быстрые свидания"]))
async def show_dates(message: Message):
    game = message.text
    async with aiosqlite.connect("bot.db") as db:
        cursor = await db.execute("SELECT datetime, kitchen, taken, max_places, price FROM events WHERE game = ? AND taken < max_places", (game,))
        rows = await cursor.fetchall()
    
    if not rows:
        await message.answer("Нет доступных дат")
        return
    
    text = f"{game} — выбери дату:\n\n"
    for dt, kitchen, taken, max_places, price in rows:
        text += f"{dt} ({kitchen})\n{taken}/{max_places} мест • {price} zł\n\n"
    await message.answer(text + "Напиши дату в формате ДД.ММ.ГГГГ ЧЧ:ММ")
