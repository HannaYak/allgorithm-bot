from aiogram import Router, types

router = Router()

@router.callback_query(lambda c: c.data == "help")
async def show_help(callback: types.CallbackQuery):
    text = (
        "Помощь\n\n"
        "• /start — главное меню\n"
        "• Игры — выбор и запись на игру\n"
        "• Личный кабинет — твои данные и лояльность\n"
        "• Оплата — Blik, карта, P24\n\n"
        "По всем вопросам: @hanna_yak\n"
        "Мы в Варшаве — ждём тебя!"
    )
    
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text="Назад", callback_data="back_to_start")]
    ])
    
    await callback.message.edit_text(text, reply_markup=keyboard, disable_web_page_preview=True)
