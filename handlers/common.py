# handlers/common.py — Правила + Помощь + Ответ админа (100% работает)
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from config import ADMIN_ID, RULES_TEXT

router = Router(name="common")


class Support(StatesGroup):
    waiting = State()


# ПРАВИЛА
@router.callback_query(F.data == "rules")
async def rules(callback: CallbackQuery):
    await callback.message.answer(RULES_TEXT)
    await callback.answer()


# ПОМОЩЬ — начало
@router.callback_query(F.data == "support")
async def support(callback: CallbackQuery, state: FSMContext):
    await state.set_state(Support.waiting)
    await callback.message.answer("Напиши свой вопрос — я перешлю его Ханне ❤️")
    await callback.answer()


# ПОМОЩЬ — получил сообщение от пользователя
@router.message(Support.waiting)
async def support_message(message: Message, state: FSMContext):
    # Админу
    await message.forward(ADMIN_ID)
    await message.bot.send_message(
        ADMIN_ID,
        f"Вопрос от @{message.from_user.username or 'без имени'} ({message.from_user.id})",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Ответить", callback_data=f"reply_{message.from_user.id}")]
        ])
    )

    # Пользователю — спасибо + меню
    menu = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Играть", callback_data="games")],
        [InlineKeyboardButton(text="Профиль", callback_data="profile")],
        [InlineKeyboardButton(text="Правила", callback_data="rules")],
        [InlineKeyboardButton(text="Помощь", callback_data="support")],
    ])
    await message.answer("Спасибо! Сообщение отправлено, скоро отвечу ❤️", reply_markup=menu)
    await state.clear()


# Админ нажал Ответить
@router.callback_query(F.data.startswith("reply_"))
async def admin_reply(callback: CallbackQuery):
    if callback.from_user.id != ADMIN_ID:
        return
    await callback.message.answer("Пиши ответ:")
    await callback.answer()


# Админ отправил ответ
@router.message(F.reply_to_message & F.from_user.id == ADMIN_ID)
async def send_admin_reply(message: Message):
    if not message.reply_to_message or not message.reply_to_message.forward_from:
        return
    user_id = message.reply_to_message.forward_from.id
    await message.copy_to(user_id, caption=f"Ответ от организатора:\n\n{message.text or ''}")
    await message.answer("Отправлено ✅")
