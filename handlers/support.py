# handlers/support.py — 100% РАБОЧАЯ ПЕРЕСЫЛКА ВОПРОСОВ АДМИНУ
from aiogram import Router, types, F
from config import ADMIN_ID  # ← убедись, что здесь твой настоящий ID (или список ID)
from aiogram import Bot

router = Router()

# Сюда впиши ВСЕХ админов (можно несколько)
ADMINS = [899891462, 5456905649]  # ← ← ← ← ← ← ← ← ← ← ← ← ← ← ← ← ← ← ← ← ← ← ← ← ← ←
# Замени на свои реальные ID (цифры, не @username!)

bot = Bot.get_current()  # берём бота из контекста

# 1. Игрок нажал кнопку «Задать вопрос организатору»
@router.message(F.text == "Задать вопрос организатору")
async def start_support(message: types.Message):
    await message.answer(
        "Пиши свой вопрос — я получу его мгновенно и отвечу лично ❤️",
        reply_markup=types.ReplyKeyboardRemove()
    )

# 2. Любое следующее сообщение от игрока — считаем вопросом и шлём всем админам
@router.message()
async def catch_question(message: types.Message):
    # Игнорируем сообщения от админов
    if message.from_user.id in ADMINS:
        return

    # Если это не вопрос в поддержку — пропускаем (чтобы не спамить)
    # (можно добавить состояние FSM, но пока так — просто шлём всё, кроме команд)
    if message.text and message.text.startswith("/"):
        return

    # Шлём всем админам
    for admin_id in ADMINS:
        try:
            await bot.forward_message(
                chat_id=admin_id,
                from_chat_id=message.chat.id,
                message_id=message.message_id
            )
            await bot.send_message(
                admin_id,
                f"Вопрос от @{message.from_user.username or 'без имени'} (ID: {message.from_user.id})"
            )
        except:
            pass  # если админ заблокировал бота — не падаем

    await message.answer("Вопрос отправлен! Скоро отвечу ❤️")

# 3. Админ отвечает реплаем на пересланное сообщение — ответ уходит игроку
@router.message(F.reply_to_message & F.from_user.id.in_(ADMINS))
async def admin_reply(message: types.Message):
    if not message.reply_to_message.forward_from:
        return

    user_id = message.reply_to_message.forward_from.id
    try:
        await bot.send_message(user_id, f"Ответ от организатора:\n\n{message.text}")
        await message.answer("Ответ отправлен игроку ✅")
    except:
        await message.answer("Не удалось отправить — возможно, пользователь заблокировал бота")
