from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from database import get_user, save_user
from datetime import datetime
from .common import main_menu

router = Router()

class Reg(StatesGroup):
    name = State()
    birth = State()
    under18 = State()
    fact = State()
    story = State()

@router.callback_query(F.data == "start_reg")
async def start_reg(callback: types.CallbackQuery, state: FSMContext):
    if await get_user(callback.from_user.id):
        await callback.answer("Ты уже в игре!", show_alert=True)
        return
    await state.set_state(Reg.name)
    await callback.message.edit_text("Как тебя зовут?")

@router.message(Reg.name)
async def get_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text.strip(), user_id=message.from_user.id)
    await state.set_state(Reg.birth)
    await message.answer("Дата рождения (ДД.ММ.ГГГГ)?")

@router.message(Reg.birth)
async def get_birth(message: types.Message, state: FSMContext):
    try:
        bdate = datetime.strptime(message.text.strip(), "%d.%m.%Y")
        age = (datetime.now() - bdate).days // 365
        await state.update_data(birth=message.text.strip(), age=age)
        if age < 18:
            await state.set_state(Reg.under18)
            await message.answer("Тебе меньше 18. Продолжить всё равно?")
        else:
            await state.set_state(Reg.fact)
            await message.answer("Факт о тебе, который никто не догадается?")
    except:
        await message.answer("Пожалуйста, формат: ДД.ММ.ГГГГ")

@router.message(Reg.under18)
async def under18_confirm(message: types.Message, state: FSMContext):
    if "да" in message.text.lower() or "продолжить" in message.text.lower():
        await state.set_state(Reg.fact)
        await message.answer("Факт о тебе, который никто не догадается?")
    else:
        await message.answer("Регистрация отменена")
        await state.clear()

@router.message(Reg.fact)
async def get_fact(message: types.Message, state: FSMContext):
    await state.update_data(fact=message.text.strip())
    await state.set_state(Reg.story)
    await message.answer("Самая странная история из твоей жизни?")

@router.message(Reg.story)
async def get_story(message: types.Message, state: FSMContext):
    data = await state.get_data()
    data["story"] = message.text.strip()
    await save_user(data)
    await message.answer("Готово! Ты в игре навсегда! 🎉", reply_markup=main_menu())
    await state.clear()
