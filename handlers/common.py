# handlers/common.py — ИСПРАВЛЕНО ПОД AIOGRAM 3.X
from aiogram import Router, F, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from config import ADMIN_ID

router = Router()

# Состояния
class SupportStates(StatesGroup):
    waiting_message = State()

# Кнопка «Помощь / Написать в поддержку»
@router.callback_query(F.data == "support")
async def support_start(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(SupportStates.waiting_message)
    await callback.message.answer(
        "Напиши свой вопрос — я сразу перешлю его организатору и скоро отвечу лично ❤️",
        reply_markup=types.ReplyKeyboardRemove()
    )
    await callback.answer()

# ←←← КРИТИЧНО: УБРАЛИ state="waiting_support" ←←←
@router.message(F.text)  # ← теперь ловит все текстовые сообщения
async def support_message_received(message: types.Message, state: FSMContext):
    # Проверяем состояние
    current_state = await state.get_state()
    if current_state != SupportStates.waiting_message:
        return  # игнорируем, если не в состоянии поддержки

    # Пересылаем админу
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Ответить", callback_data=f"reply_{message.from_user.id}")]
    ])
    await message.forward(ADMIN_ID)
    await message.bot.send_message(
        ADMIN_ID,
        f"Вопрос от @{message.from_user.username or 'без username'} ({message.from_user.id})",
        reply_markup=kb
    )

    # Возвращаем пользователя в главное меню
    main_kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Играть", callback_data="games")],
        [InlineKeyboardButton(text="Мой профиль", callback_data="profile")],
        [InlineKeyboardButton(text="Правила", callback_data="rules")],
        [InlineKeyboardButton(text="Помощь", callback_data="support")],
    ])

    await message.answer(
        "Спасибо! Твоё сообщение отправлено.\n"
        "Я скоро отвечу лично ❤️",
        reply_markup=main_kb
    )
    await state.clear()  # выходим из состояния

# Админ нажал «Ответить»
@router.callback_query(F.data.startswith("reply_"))
async def admin_reply(callback: types.CallbackQuery):
    if callback.from_user.id != ADMIN_ID:
        return await callback.answer("Ты не админ", show_alert=True)

    await callback.message.answer(f"Пиши ответ пользователю {callback.data.split('_')[1]}:")
    await callback.answer()

# Админ отправил ответ (ответил на пересланное сообщение)
@router.message(F.reply_to_message & F.from_user.id == ADMIN_ID)
async def send_reply_to_user(message: types.Message):
    if not message.reply_to_message or not message.reply_to_message.forward_from:
        return

    user_id = message.reply_to_message.forward_from.id
    await message.bot.send_message(user_id, f"Ответ от организатора:\n\n{message.text}")
    await message.answer("Ответ отправлен ✅")
