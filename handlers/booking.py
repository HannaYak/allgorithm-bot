from aiogram import Router, types
from .common import is_registered

router = Router()

@router.callback_query(lambda c: c.data.startswith("event_"))
async def show_event_rules(callback: types.CallbackQuery):
    if not await is_registered(callback): return

    rules = {
        "eatmeet": "Встреча незнакомцев в ресторане. Бот раскрывает место за 3 часа. Темы и мини-игры.",
        "auction": "Твоя странная история зачитывается анонимно — угадываем автора!",
        "stock": "3 подсказки, ставки вживую. Победитель забирает банк.",
        "speed": "15 минут на пару. Контакты только при взаимной симпатии через бота."
    }
    key = callback.data.split("_")[1]
    kb = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text="Продолжить бронирование →", callback_data=f"pay_{key}")],
        [types.InlineKeyboardButton(text="Назад", callback_data="events")]
    ])
    await callback.message.edit_text(rules.get(key, "Скоро будет"), reply_markup=kb)
