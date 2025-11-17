# handlers/start.py — ФИНАЛЬНАЯ РАБОЧАЯ ВЕРСИЯ (aiogram 3.13+)
from aiogram import Router, types, F
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from database import add_user

router = Router()

class RegisterStates(StatesGroup):
    waiting_name = State()
    waiting_age = State()

# ==================== /start ====================
@router.message(CommandStart())
async def cmd_start(message: types.Message, state: FSMContext):
    kb = types.ReplyKeyboardMarkup(
        keyboard=[[types.KeyboardButton(text="Начать")]],
        resize_keyboard=True,
        one_time_keyboard=True
    )
    
    await message.answer(
        "Привет! 👋\n\n"
        "Я — бот для самых крутых игр в Варшаве 🎉\n"
        "Нажми кнопку ниже, и мы познакомимся!",
        reply_markup=kb
    )
    await state.clear()

# ==================== КНОПКА "НАЧАТЬ" ====================
@router.message(F.text == "Начать")
async def start_registration(message: types.Message, state: FSMContext):
    await message.answer(
        "Супер! Давай знакомиться 😊\n\nКак тебя зовут?",
        reply_markup=types.ReplyKeyboardRemove()
    )
    await state.set_state(RegisterStates.waiting_name)

# Имя
@router.message(RegisterStates.waiting_name)
async def get_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text.strip())
    await message.answer("Отлично! А сколько тебе лет?")
    await state.set_state(RegisterStates.waiting_age)

# Возраст → завершаем и показываем меню
@router.message(RegisterStates.waiting_age)
async def get_age(message: types.Message, state: FSMContext):
    if not message.text.isdigit() or not (16 <= int(message.text) <= 99):
        return await message.answer("Пожалуйста, пришли возраст цифрами (например, 27)")

    data = await state.get_data()
    name = data.get("name", "Друг")
    
    await add_user(message.from_user.id, name=name, age=int(message.text))
    
    await message.answer(
        f"Привет, {name}! Тебе {message.text} лет — идеально для наших игр 🔥\n\n"
        "Теперь ты в системе! Выбери, что хочешь:",
        reply_markup=main_menu_keyboard()
    )
    await state.clear()

# ==================== ГЛАВНОЕ МЕНЮ ====================
def main_menu_keyboard():
    keyboard = [
        [types.KeyboardButton(text="Игры")],
        [types.KeyboardButton(text="Личный кабинет"), types.KeyboardButton(text="Помощь")],
        [types.KeyboardButton(text="Правила")]
    ]
    return types.ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

# /menu и кнопка "Меню"
@router.message(Command("menu"))
@router.message(F.text == "Меню")
async def cmd_menu(message: types.Message):
    await message.answer("Главное меню:", reply_markup=main_menu_keyboard())

# ==================== ПРАВИЛА ====================
@router.message(F.text == "Правила")
async def show_rules(message: types.Message):
    rules = (
        "Общие правила\n\n"
        "1. Все игры — в уютных локациях Варшавы\n"
        "2. Оплата через бота (Blik, карта, P24)\n"
        "3. После оплаты — ты в игре автоматически\n"
        "4. За 5 игр — следующая со скидкой 20%\n"
        "5. Отмена возможна за 24ч до игры\n\n"
        "По вопросам: @hanna_yak"
    )
    await message.answer(rules, reply_markup=main_menu_keyboard())
