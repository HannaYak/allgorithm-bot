from aiogram import Router, types
from .common import is_registered, main_menu

router = Router()

@router.callback_query(lambda c: c.data == "events")
async def show_events(callback: types.CallbackQuery):
    if not await is_registered(callback): return

    kb = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text="Eat & Meet / Talk & Toast", callback_data="event_eatmeet")],
        [types.InlineKeyboardButton(text="Аукцион странных историй", callback_data="event_auction")],
        [types.InlineKeyboardButton(text="Stock & Know", callback_data="event_stock")],
        [types.InlineKeyboardButton(text="Быстрые свидания", callback_data="event_speed")],
        [types.InlineKeyboardButton(text="Назад", callback_data="back_main")]
    ])
    await callback.message.edit_text("Выбери мероприятие:", reply_markup=kb)
