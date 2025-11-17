# handlers/support.py — ФИНАЛЬНАЯ ВЕРСИЯ, РАБОТАЕТ ВЕЗДЕ
from aiogram import Router, types, F, Bot

router = Router()

# ←←← ВПИШИ СВОИ АДМИНСКИЕ ID СЮДА (цифры!)
ADMINS = [5456905649, 899891462]   # ←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←

# 1. Нажал кнопку → ждём вопрос
@router.message(F.text == "Задать вопрос организатору")
async def start_support(message: types.Message):
    await message.answer(
        "Пиши свой вопрос — я получу его мгновенно и отвечу лично ❤️",
        reply_markup=types.ReplyKeyboardRemove()
    )

# 2. Любое сообщение после этого — считаем вопросом
@router.message()
async def catch_question(message: types.Message, bot: Bot):
    # Игнорируем админов
    if message.from_user.id in ADMINS:
        return

    # Игнорируем команды
    if message.text and message.text.startswith("/"):
        return

    # Пересылаем ВСЕМ админам
    for admin_id in ADMINS:
        try:
            await bot.forward_message(admin_id, message.chat.id, message.message_id)
            await bot.send_message(
                admin_id,
                f"Вопрос от @{message.from_user.username or 'без имени'} (ID: {message.from_user.id})"
            )
        except Exception as e:
            print(f"Не смог отправить админу {admin_id}: {e}")

    await message.answer("Вопрос отправлен! Скоро отвечу ❤️")

# 3. Админ ответил реплаем → ответ уходит игроку
@router.message(F.reply_to_message & F.from_user.id.in_(ADMINS))
async def admin_reply(message: types.Message, bot: Bot):
    if not message.reply_to_message or not message.reply_to_message.forward_from:
        return

    user_id = message.reply_to_message.forward_from.id
    try:
        await bot.send_message(user_id, f"Ответ от организатора:\n\n{message.text}")
        await message.answer("Ответ отправлен игроку ✅")
    except Exception:
        await message.answer("Не удалось отправить — игрок заблокировал бота")
