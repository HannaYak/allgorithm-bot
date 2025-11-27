# handlers/help.py — ПРОСТАЯ ПОМОЩЬ
from aiogram import Router, types, F

router = Router()

@router.message(F.text == "Помощь")
async def help_simple(message: types.Message):
    text = (
        "Помощь\n\n"
        "• /start — начать заново\n"
        "• /menu — главное меню\n"
        "• Игры — выбрать игру\n"
        "• Личный кабинет — твоя карта лояльности\n"
        "• Правила — общие правила\n\n"
        "Нужна помощь лично от меня? Нажми кнопку ниже ↓"
    )
    
    kb = [[types.KeyboardButton(text="Задать вопрос организатору")]]
    await message.answer(text, reply_markup=types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True))
