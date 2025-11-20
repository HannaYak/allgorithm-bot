# handlers/support.py — теперь отвечает и за Правила, и за Помощь
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from config import ADMIN_ID, RULES_TEXT

router = Router(name="support_and_rules")

ADMIN_ID = [5456905649]

class SupportState(StatesGroup):
    waiting = State()


# ——— КНОПКА «ПРАВИЛА» ———
@router.callback_query(F.data == "rules")
async def show_rules(callback: CallbackQuery):
    await callback.message.answer(RULES_TEXT, disable_web_page_preview=True)
    await callback.answer()


# ——— КНОПКА «ПОМОЩЬ» ———
@router.callback_query(F.data == "support")
async def support_start(callback: CallbackQuery, state: FSMContext):
    await state.set_state(SupportState.waiting)
    await callback.message.answer(
        "Напиши свой вопрос — я сразу перешлю Ханне и скоро отвечу лично ❤️"
    )
    await callback.answer()


# ——— ПОЛЬЗОВАТЕЛЬ ОТПРАВИЛ СООБЩЕНИЕ В ПОДДЕРЖКУ ———
@router.message(SupportState.waiting)
async def get_support_message(message: Message, state: FSMContext):
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Ответить", callback_data=f"reply_{message.from_user.id}")]
    ])
    await message.forward(ADMIN_ID)
    await message.bot.send_message(
        ADMIN_ID,
        f"Вопрос от @{message.from_user.username or 'без username'} ({message.from_user.id})",
        reply_markup=kb
    )

    # Возврат в главное меню
    menu = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Играть", callback_data="games")],
        [InlineKeyboardButton(text="Мой профиль", callback_data="profile")],
        [InlineKeyboardButton(text="Правила", callback_data="rules")],
        [InlineKeyboardButton(text="Помощь", callback_data="support")],
    ])

    await message.answer(
        "Спасибо! Сообщение отправлено.\nЯ скоро отвечу лично ❤️",
        reply_markup=menu
    )
    await state.clear()


# ——— ОТВЕТ АДМИНА ———
@router.callback_query(F.data.startswith("reply_"))
async def admin_reply(callback: CallbackQuery):
    if callback.from_user.id != ADMIN_ID:
        return await callback.answer("❌", show_alert=True)
    await callback.message.answer("Пиши ответ:")
    await callback.answer()

@router.message(F.reply_to_message, F.from_user.id == ADMIN_ID)
async def send_reply(message: Message):
    if not message.reply_to_message.forward_from:
        return
    user_id = message.reply_to_message.forward_from.id
    await message.bot.send_message(user_id, f"Ответ от организатора:\n\n{message.text}")
    await message.answer("Отправлено ✅")
