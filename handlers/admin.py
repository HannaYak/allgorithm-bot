from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from config import ADMIN_ID
from database import init_db
import aiosqlite
from datetime import datetime, timedelta

router = Router()

class Admin(StatesGroup):
    type = State()
    date = State()
    time = State()
    place = State()
    price = State()

@router.message(F.from_user.id == ADMIN_ID, F.text == "/admin")
async def admin_panel(message: types.Message, state: FSMContext):
    kb = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text="Добавить даты на 2 недели", callback_data="add_events")],
        [types.InlineKeyboardButton(text="Посмотреть все записи", callback_data="view_all_bookings")],
    ])
    await message.answer("Админ-панель 🔥", reply_markup=kb)

@router.callback_query(F.data == "add_events", F.from_user.id == ADMIN_ID)
async def start_add_events(callback: types.CallbackQuery, state: FSMContext):
    kb = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text="Eat & Meet", callback_data="add_eatmeet")],
        [types.InlineKeyboardButton(text="Аукцион историй", callback_data="add_auction")],
        [types.InlineKeyboardButton(text="Stock & Know", callback_data="add_stock")],
        [types.InlineKeyboardButton(text="Быстрые свидания", callback_data="add_speed")],
    ])
    await callback.message.edit_text("Выбери тип мероприятия:", reply_markup=kb)

@router.callback_query(F.data.startswith("add_"), F.from_user.id == ADMIN_ID)
async def choose_type(callback: types.CallbackQuery, state: FSMContext):
    await state.update_data(type=callback.data[4:])
    await state.set_state(Admin.date)
    await callback.message.edit_text("Дата начала (ДД.ММ.ГГГГ):")

@router.message(Admin.date, F.from_user.id == ADMIN_ID)
async def get_date(message: types.Message, state: FSMContext):
    await state.update_data(date=message.text.strip())
    await state.set_state(Admin.time)
    await message.answer("Время (например 19:30):")

@router.message(Admin.time, F.from_user.id == ADMIN_ID)
async def get_time(message: types.Message, state: FSMContext):
    await state.update_data(time=message.text.strip())
    data = await state.get_data()
    if data["type"] == "eatmeet":
        await state.set_state(Admin.place)
        await message.answer("Ресторан (скроется до -3 часов):")
    else:
        await state.set_state(Admin.price)
        await message.answer("Цена (PLN):")

@router.message(Admin.place, F.from_user.id == ADMIN_ID)
async def get_place(message: types.Message, state: FSMContext):
    await state.update_data(place=message.text.strip())
    await state.set_state(Admin.price)
    await message.answer("Цена (PLN):")

@router.message(Admin.price, F.from_user.id == ADMIN_ID)
async def save_events(message: types.Message, state: FSMContext):
    data = await state.get_data()
    base_date = datetime.strptime(data["date"], "%d.%m.%Y")
    
    async with aiosqlite.connect("bot.db") as db:
        for i in range(14):  # 2 недели
            event_date = base_date + timedelta(days=i)
            dt_str = event_date.strftime("%d.%m.%Y") + " " + data["time"]
            place = data.get("place", "Будет объявлено за 3 часа")
            await db.execute("""
                INSERT INTO events (type, datetime, place, price)
                VALUES (?, ?, ?, ?)
            """, (data["type"], dt_str, place, int(message.text)))
        await db.commit()
    
    await message.answer(f"Добавлено 14 дат для {data['type']}!")
    await state.clear()
