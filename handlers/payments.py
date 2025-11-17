# handlers/payments.py — ПОЛНОСТЬЮ РАБОЧИЙ, БЕЗ ОШИБОК
from aiogram import Router, types, F
import aiosqlite

router = Router()

PAYMENT_LINKS = {
    "meet_eat": "https://buy.stripe.com/8x26oHcyf0RBaHico50sU03",
    "lock_stock": "https://buy.stripe.com/3cIeVd7dVeIr9De2Nv0sU02",
    "bar_liar": "https://buy.stripe.com/00w5kDgOv2ZJbLm87P0sU01",
    "speed_dating": "https://book.stripe.com/aFa3cv1TBgQzbLm5ZH0sU00",
}

@router.callback_query(lambda c: c.data and c.data.startswith("pay:"))
async def process_payment(callback: types.CallbackQuery):
    game_key = callback.data.split(":")[1]
    
    # Проверяем, есть ли места
    async with aiosqlite.connect("bot.db") as db:
        db.row_factory = aiosqlite.Row
        async with db.execute("SELECT seats_taken, seats_total, name FROM games WHERE key = ?", (game_key,)) as cur:
            game = await cur.fetchone()
    
    if not game:
        await callback.answer("Игра не найдена!", show_alert=True)
        return
    
    if game["seats_taken"] >= game["seats_total"]:
        await callback.answer("Мест уже нет!", show_alert=True)
        return
    
    link = PAYMENT_LINKS.get(game_key)
    if not link or link.startswith("https://buy.stripe.com/твоя"):
        await callback.message.edit_text("Оплата временно недоступна. Напиши @hanna_yak")
        return
    
    kb = [[types.InlineKeyboardButton(text=f"Оплатить {game['name']} — сейчас только за 10 секунд!", url=link)]]
    
    await callback.message.edit_text(
        f"Ты выбрал: *{game['name']}*\n\n"
        f"После оплаты ты автоматически записан на игру!\n"
        f"Осталось мест: {game['seats_total'] - game['seats_taken']}",
        reply_markup=types.InlineKeyboardMarkup(inline_keyboard=kb),
        parse_mode="Markdown"
    )

