from aiogram import Router, types, F

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

@router.message(F.text == "Помощь")
async def help_from_menu(message: types.Message):
    await message.answer(
        "Помощь\n\n"
        "• /start — начать заново\n"
        "• /menu — главное меню\n"
        "• По вопросам: @hanna_yak"
    )
    
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text="Назад", callback_data="back_to_start")]
    ])
    
    await callback.message.edit_text(text, reply_markup=keyboard, disable_web_page_preview=True)
