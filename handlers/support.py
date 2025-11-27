from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from config import ADMIN_ID
from .common import main_menu, is_registered

router = Router()

class Support(StatesGroup):
    waiting = State()

@router.callback_query(F.data == "support")
async def support_start(callback: types.CallbackQuery, state: FSMContext):
    if not await is_registered(callback): return
    await state.set_state(Support.waiting)
    await callback.message.edit_text("Напиши свой вопрос — отвечу лично ❤️")

@router.message(Support.waiting)
async def support_message(message: types.Message, state: FSMContext):
    await bot.forward_message(ADMIN_ID, message.from_user.id, message.message_id)
    await bot.send_message(ADMIN_ID, f"Вопрос от @{message.from_user.username or message.from_user.id}")
    
    await message.answer("Спасибо! Скоро отвечу лично ❤️", reply_markup=main_menu())
    await state.clear()
