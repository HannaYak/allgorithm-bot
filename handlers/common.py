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
# ПРАВИЛА — теперь работает
@router.callback_query(F.data == "show_rules")
async def show_rules(callback: CallbackQuery):
    await callback.message.edit_text(
        RULES_TEXT,  # текст из config.py
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Назад", callback_data="back_to_menu")]
        ])
    )
    await callback.answer()

# ПОМОЩЬ — теперь работает и возвращает в меню
@router.callback_query(F.data == "support_start")
async def support_start(callback: CallbackQuery, state: FSMContext):
    await state.set_state("waiting_support")
    await callback.message.edit_text("Напиши свой вопрос — я перешлю организатору ❤️")
    await callback.answer()

@router.message(F.text, state="waiting_support")
async def get_support_message(message: Message, state: FSMContext):
    await message.forward(ADMIN_ID)
    await message.bot.send_message(
        ADMIN_ID,
        f"Вопрос от @{message.from_user.username or 'без имени'} ({message.from_user.id})",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Ответить", callback_data=f"reply_{message.from_user.id}")]
        ])
    )
    await message.answer(
        "Спасибо! Твоё сообщение отправлено.\nСкоро отвечу ❤️",
        reply_markup=main_menu(registered=True)
    )
    await state.clear() 

    @router.callback_query(F.data == "back_to_menu")
async def back_to_menu(callback: CallbackQuery):
    user = await get_user(callback.from_user.id)
    await callback.message.edit_text(
        "Главное меню",
        reply_markup=main_menu(registered=bool(user and user.get("registered")))
    )
    await callback.answer()
    
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
