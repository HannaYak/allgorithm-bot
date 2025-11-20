# handlers/admin_support.py
from aiogram import Router, F, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from config import ADMIN_ID

router = Router()

# Пользователь пишет в «Техподдержку» или просто в личку боту
@router.message(F.chat.type == "private")
async def forward_to_admin(message: types.Message):
    if message.from_user.id == ADMIN_ID:
        return  # админ сам себе не форвардим

    # Пересылаем админу
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Ответить", callback_data=f"reply_{message.from_user.id}")]
    ])
    await message.forward(chat_id=ADMIN_ID)
    await message.bot.send_message(
        ADMIN_ID,
        f"↑ Сообщение от @{message.from_user.username or 'без юзернейма'} ({message.from_user.id})",
        reply_markup=kb
    )
    await message.answer("Ваше сообщение отправлено в поддержку. Скоро ответим!")

# Админ нажимает «Ответить»
@router.callback_query(F.data.startswith("reply_"))
async def reply_to_user(callback: types.CallbackQuery):
    if callback.from_user.id != ADMIN_ID:
        return await callback.answer("Ты не админ!")

    user_id = int(callback.data.split("_")[1])
    await callback.message.answer(f"Пиши ответ пользователю {user_id}:")
    await callback.message.bot.send_message(
        ADMIN_ID,
        "Ответ отправлен будет этому пользователю",
        reply_markup=None
    )
    
    # Сохраняем, кому админ сейчас отвечает
    await callback.message.bot.send_message(
        ADMIN_ID,
        f"/reply_{user_id} текст_ответа",
        reply_markup=None
    )
    await callback.answer()

# Админ отправляет ответ через команду или просто текст после нажатия кнопки
@router.message(F.text.startswith("/reply_") | F.reply_to_message)
async def send_reply(message: types.Message):
    if message.from_user.id != ADMIN_ID:
        return

    # Если использует команду /reply_123456789 текст
    if message.text.startswith("/reply_"):
        try:
            user_id = int(message.text.split()[0].split("_")[1])
            reply_text = message.text.split(" ", 1)[1] if len(message.text.split()) > 1 else "."
        except:
            return await message.answer("Формат: /reply_123456789 Привет!")
    else:
        # Если просто ответил на пересланное сообщение
        if not message.reply_to_message or not message.reply_to_message.forward_from:
            return
        user_id = message.reply_to_message.forward_from.id
        reply_text = message.text

    await message.bot.send_message(user_id, f"Ответ от поддержки:\n\n{reply_text}")
    await message.answer(f"Ответ отправлен пользователю {user_id}")

