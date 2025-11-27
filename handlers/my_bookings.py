from aiogram import Router, types
from .common import is_registered

router = Router()

@router.callback_query(lambda c: c.data == "my_bookings")
async def my_bookings(callback: types.CallbackQuery):
    if not await is_registered(callback): return

    await callback.message.edit_text(
        "Твои записи:\n\n"
        "Пока пусто. Запишись на мероприятие в разделе «Мероприятия»",
        reply_markup=types.InlineKeyboardMarkup(inline_keyboard=[
            [types.InlineKeyboardButton(text="Назад", callback_data="back_main")]
        ])
    )
