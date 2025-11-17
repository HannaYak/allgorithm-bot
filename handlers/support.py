# handlers/support.py — ТОЛЬКО ПО КНОПКЕ "Задать вопрос"
from aiogram import Router, types, F
from config import ADMIN_ID, bot

router = Router()

# Пользователь нажал "Задать вопрос организатору"
@router.message(F.text == "Задать вопрос организатору")
async def ask_support(message: types.Message):
    await message.answer(
        "Пиши свой вопрос — я получу его мгновенно и отвечу лично ❤️",
        reply_markup=types.ReplyKeyboardRemove()
    )

# Любое следующее сообщение — считаем вопросом и пересылаем тебе
@router.message(F.reply_to_message & F.reply_to_message.text.contains("Пиши свой вопрос"))
async def forward_question(message: types.Message):
    # Пересылаем тебе
    await bot.forward_message(
        chat_id=ADMIN_ID,
        from_chat_id=message.from_user.id,
        message_id=message.message_id
    )
    await bot.send_message(
        ADMIN_ID,
        f"Вопрос от @{message.from_user.username or 'без имени'} (ID: {message.from_user.id})"
    )
    
    await message.answer("Вопрос отправлен! Скоро отвечу ❤️")

# Ты отвечаешь реплаем на пересланное сообщение — ответ уходит игроку
@router.message(F.reply_to_message & F.from_user.id == ADMIN_ID)
async def admin_reply(message: types.Message):
    if not message.reply_to_message.forward_from:
        return
    
    user_id = message.reply_to_message.forward_from.id
    await bot.send_message(user_id, f"Ответ от организатора:\n\n{message.text}")
    await message.answer("Ответ отправлен игроку")
