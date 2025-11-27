from aiogram import Router, types
from .common import is_registered

router = Router()

@router.callback_query(lambda c: c.data == "rules")
async def show_rules(callback: types.CallbackQuery):
    if not await is_registered(callback): return

    await callback.message.edit_text(
        "Общие правила:\n\n"
        "• Оплата невозвратная за 48 часов\n"
        "• Приходи вовремя — ждём 15 минут\n"
        "• Уважай участников\n\n"
        "Правила каждого мероприятия — показываются при выборе",
        reply_markup=types.InlineKeyboardMarkup(inline_keyboard=[
            [types.InlineKeyboardButton(text="Назад", callback_data="back_main")]
        ])
    )
