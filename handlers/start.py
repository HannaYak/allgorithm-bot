# handlers/start.py — НОВАЯ ЛОГИКА С КНОПКОЙ "НАЧАТЬ"
from aiogram import Router, types, F
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

router = Router()

# Состояния анкеты
class RegisterStates(StatesGroup):
    waiting_name = State()
    waiting_age = State()

# ==================== /start ====================
@router.message(CommandStart())
async def cmd_start(message: types.Message, state: FSMContext):
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    kb.add(types.KeyboardButton(text="Начать"))

    await message.answer(
        "Привет! 👋\n\n"
        "Я — бот для крутых игр в Варшаве 🎉\n"
        "Нажми кнопку ниже, и мы начнём знакомство!",
        reply_markup=kb
    )
    await state.clear()  # на всякий случай

# ==================== КНОПКА "НАЧАТЬ" ====================
@router.message(F.text == "Начать")
async def start_registration(message: types.Message, state: FSMContext):
    await message.answer(
        "Отлично! Давай познакомимся 😊\n\nКак тебя зовут?",
        reply_markup=types.ReplyKeyboardRemove()
    )
    await state.set_state(RegisterStates.waiting_name)

# Имя
@router.message(RegisterStates.waiting_name)
async def get_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text.strip())
    await message.answer("Супер! А сколько тебе лет?")
    await state.set_state(RegisterStates.waiting_age)

# Возраст → завершаем анкету и показываем главное меню
@router.message(RegisterStates.waiting_age)
async def get_age(message: types.Message, state: FSMContext):
    if not message.text.isdigit() or not (10 <= int(message.text) <= 99):
        return await message.answer("Пожалуйста, пришли возраст цифрами (например, 25)")

    data = await state.get_data()
    name = data.get("name", "Друг")
    age = message.text

    from database import add_user
    await add_user(message.from_user.id, name=name, age=int(age))

    await message.answer(
        f"Привет, {name}! Тебе {age} лет — идеально для наших игр 🔥\n\n"
        "Теперь ты в системе! Выбери, что хочешь:",
        reply_markup=main_menu_keyboard()
    )
    await state.clear()

# ==================== ГЛАВНОЕ МЕНЮ (4 КНОПКИ) ====================
def main_menu_keyboard():
    kb = [
        [types.KeyboardButton(text="Игры")],
        [types.KeyboardButton(text="Личный кабинет"), types.KeyboardButton(text="Помощь")],
        [types.KeyboardButton(text="Правила")]
    ]
    return types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)

# Команда /menu и кнопка "Меню" (на всякий случай)
@router.message(Command("menu"))
@router.message(F.text == "Меню")
async def show_menu(message: types.Message):
    await message.answer("Главное меню:", reply_markup=main_menu_keyboard())

# ==================== ПРАВИЛА (ОБЩИЕ) ====================
@router.message(F.text == "Правила")
async def show_rules(message: types.Message):
    rules_text = (
        "Общие правила бота\n\n"
        "1. Все игры проходят в Варшаве в уютных локациях\n"
        "2. Оплата только через бота (Blik, карта, P24)\n"
        "3. После оплаты — ты автоматически в игре\n"
        "4. За 5 посещений — следующая игра со скидкой 20%\n"
        "5. Отмена возможна за 24 часа до игры\n\n"
        "По всем вопросам — @hanna_yak"
    )
    kb = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text="Вернуться в меню", callback_data="back_to_menu")]
    ])
    await message.answer(rules_text, reply_markup=kb)

@router.callback_query(F.data == "back_to_menu")
async def back_to_menu(callback: types.CallbackQuery):
    await callback.message.edit_text(
        "Главное меню:",
        reply_markup=None
    )
    await callback.message.answer("Выбери:", reply_markup=main_menu_keyboard())
