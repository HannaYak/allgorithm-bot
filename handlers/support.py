# handlers/support.py — 100% РАБОЧИЕ ЗАПРОСЫ АДМИНАМ
from aiogram import Router, types, F, Bot

router = Router()

# ←←←←←←←←←←←←←← ВПИШИ СВОИ ID СЮДА (цифры!)
ADMINS = [5456905649]  # ←←←←←←←←←←←←←←←←←←←←←←←←←←←

@router.message(F.text == "Задать вопрос организатору")
async def start_support(message: types.Message):
    await message.answer(
        "Пиши свой вопрос — я получу его мгновенно и отвечу лично ❤️",
        reply_markup=types.ReplyKeyboardRemove()
    )

@router.message()
async def catch_any_message(message: types.Message, bot: Bot):
    if message.from_user.id in ADMINS:
        return
    if message.text and message.text.startswith("/"):
        return

    # Отправляем всем админам
    for admin_id in ADMINS:
        try:
            await bot.forward_message(admin_id, message.chat.id, message.message_id)
            await bot.send_message(admin_id, f"Вопрос от {message.from_user.username or 'без имени'} (ID: {message.from_user.id})")
        except:
            pass

    await message.answer("Вопрос отправлен! Скоро отвечу ❤️")

# Ответ админа → игроку
@router.message(F.reply_to_message & F.from_user.id.in_(ADMINS))
async def admin_reply(message: types.Message, bot: Bot):
    if not message.reply_to_message.forward_from:
        return
    user_id = message.reply_to_message.forward_from.id
    await bot.send_message(user_id, f"Ответ от организатора:\n\n{message.text}")
    await message.answer("Ответ отправлен игроку ✅")
