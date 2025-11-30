from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from database import init
import aiosqlite

router = Router()

class Reg(StatesGroup):
    name = State()
    birth = State()
    fact = State()
    story = State()

@router.message(F.text == "Начать анкету")
async def start_reg(message: Message, state: FSMContext):
    await state.set_state(Reg.name)
    await message.answer("1/5 — Как тебя зовут?")

@router.message(Reg.name)
async def get_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(Reg.birth)
    await message.answer("2/5 — Дата рождения (ДД.ММ.ГГГГ)")

@router.message(Reg.birth)
async def get_birth(message: Message, state: FSMContext):
    await state.update_data(birth=message.text)
    await state.set_state(Reg.fact)
    await message.answer("3/5 — Факт о тебе, который никто не догадается")

@router.message(Reg.fact)
async def get_fact(message: Message, state: FSMContext):
    await state.update_data(fact=message.text)
    await state.set_state(Reg.story)
    await message.answer("4/5 — Самая странная история из жизни")

@router.message(Reg.story)
async def finish_reg(message: Message, state: FSMContext):
    data = await state.get_data()
    async with aiosqlite.connect("bot.db") as db:
        await db.execute(
            "INSERT OR REPLACE INTO users (id, name, birth, fact, story) VALUES (?, ?, ?, ?, ?)",
            (message.from_user.id, data['name'], data['birth'], data['fact'], message.text)
        )
        await db.commit()
    await state.clear()
    await message.answer("Готово! Ты в игре навсегда ✨", reply_markup=main_menu())
