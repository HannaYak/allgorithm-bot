# handlers/support.py — ПОДДЕРЖКА: ПОЛЬЗОВАТЕЛЬ ↔ АДМИН
from aiogram import Router, types, F
from config import ADMIN_ID, bot

router = Router()

# Все сообщения, которые не попали под другие хендлеры — считаем вопросом в поддержку
@router.message()
async def forward_to_admin(message: types.Message):
    if message.from_user.id == ADMIN_ID:
        return  # админ сам себе не пересылает

    # Пересылаем админу
    await bot.send_message(
        ADMIN_ID,
        f"Вопрос от @{message.from_user.username or 'без юзернейма'} (ID: {message.from_user.id})\n\n"
        f"{message.text or 'голосовое/стикер/фото'}"
    )
    if message.text:
        await bot.forward_message(ADMIN_ID, message.from_user.id, message.message_id)

    await message.answer("Твой вопрос отправлен! Скоро отвечу ❤️")

# Админ отвечает — ответ уходит пользователю
@router.message(F.reply_to_message & F.from_user.id == ADMIN_ID)
async def reply_to_user(message: types.Message):
    if not message.reply_to_message or not message.reply_to_message.forward_from:
        return

    user_id = message.reply_to_message.forward_from.id
    await bot.send_message(user_id, f"Ответ от организатора:\n\n{message.text}")
    await message.answer("Ответ отправлен пользователю")
