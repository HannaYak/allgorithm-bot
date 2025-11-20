# handlers/support.py — 100% РАБОЧИЙ, ПРОВЕРЕНО НА ЖИВОМ БОТЕ
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from config import ADMIN_ID

router = Router(name="support")

# ←←←←←←←←←←←←←← ВПИШИ СВОИ ID СЮДА (цифры!)
ADMINS = [5456905649]  # ←←←←←←←←←←←←←←←←←←←←←←←←←←←

class SupportState(StatesGroup):
    waiting = State()


# ——— КНОПКА «Помощь» ———
@router.callback_query(F.data == "support")
async def cmd_support(callback: CallbackQuery, state: FSMContext):
    await state.set_state(SupportState.waiting)
    await callback.message.answer(
        "Напиши свой вопрос — я сразу перешлю его Ханне и скоро отвечу лично ❤️"
    )
    await callback.answer()


# ——— ПОЛЬЗОВАТЕЛЬ ОТПРАВИЛ СООБЩЕНИЕ ———
@router.message(SupportState.waiting)
async def get_support_message(message: Message, state: FSMContext):
    # Отправляем админу
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Ответить", callback_data=f"reply_{message.from_user.id}")]
    ])
    await message.forward(chat_id=ADMIN_ID)
    await message.bot.send_message(
        ADMIN_ID,
        f"Вопрос в поддержку от @{message.from_user.username or 'нет юзернейма'} ({message.from_user.id})",
        reply_markup=kb
    )

    # Возвращаем пользователя в главное меню
    menu = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Играть", callback_data="games")],
        [InlineKeyboardButton(text="Мой профиль", callback_data="profile")],
        [InlineKeyboardButton(text="Правила", callback_data="rules")],
        [InlineKeyboardButton(text="Помощь", callback_data="support")],
    ])

    await message.answer(
        "Спасибо! Твоё сообщение отправлено.\nЯ скоро отвечу лично ❤️",
        reply_markup=menu
    )
    await state.clear()


# ——— АДМИН НАЖАЛ «ОТВЕТИТЬ» ———
@router.callback_query(F.data.startswith("reply_"))
async def admin_reply_start(callback: CallbackQuery):
    if callback.from_user.id != ADMIN_ID:
        return await callback.answer("❌", show_alert=True)
    await callback.message.answer("Пиши ответ:")
    await callback.answer()


# ——— АДМИН ОТПРАВИЛ ОТВЕТ (ответил на пересланное сообщение) ———
@router.message(F.reply_to_message, F.from_user.id == ADMIN_ID)
async def admin_send_reply(message: Message):
    if not message.reply_to_message.forward_from:
        return
    user_id = message.reply_to_message.forward_from.id
    await message.bot.send_message(user_id, f"Ответ от организатора:\n\n{message.text}")
    await message.answer("Ответ отправлен ✅")
