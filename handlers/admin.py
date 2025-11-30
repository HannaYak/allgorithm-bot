from aiogram import Router, F
from aiogram.types import Message
from config import ADMIN_ID
import aiosqlite
import uuid

router = Router()

@router.message(F.from_user.id == ADMIN_ID)
async def admin_add_event(message: Message):
    try:
        game, dt, kitchen, loc, limit, price = message.text.split(" | ")
        event_id = str(uuid.uuid4())[:8]
        async with aiosqlite.connect("bot.db") as db:
            await db.execute(
                "INSERT INTO events (id, game, datetime, kitchen, location, limit, price) VALUES (?, ?, ?, ?, ?, ?, ?)",
                (event_id, game.strip(), dt.strip(), kitchen.strip(), loc.strip(), int(limit), int(price))
            )
            await db.commit()
        await message.answer("Событие добавлено!")
    except Exception as e:
        await message.answer(f"Ошибка: {e}\nФормат: Игра | ДД.ММ.ГГГГ ЧЧ:ММ | Кухня | Адрес | Лимит | Цена")
