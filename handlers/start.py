# handlers/start.py — РЕГИСТРАЦИЯ 18+ С ТВОИМИ КРУТЫМИ ВОПРОСАМИ
from aiogram import Router, types, F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from database import get_user, add_user
from datetime import datetime

router = Router()

class Register(StatesGroup):
    waiting_name = State()
    waiting_birthdate = State()
    waiting_under18_confirm = State()
    waiting_fun_fact = State()
    waiting_crazy_story = State()

def main_menu_keyboard():
    kb = [
        [types.KeyboardButton(text="Игры")],
        [types.KeyboardButton(text="Личный кабинет")],
        [types.KeyboardButton(text="Помощь"), types.KeyboardButton(text="Правила")]
    ]
    return types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)

@router.message(CommandStart())
async def cmd_start(message: types.Message, state: FSMContext):
    user = await get_user(message.from_user.id)
    if user and user.get("name") and user.get("birthdate"):
        await message.answer(
            f"С возвращением, {user['name']}! ❤️\nТы уже в игре!",
            reply_markup=main_menu_keyboard()
        )
        return

    await message.answer(
        "Привет! Я бот для самых крутых игр в Варшаве 🥂\n\n"
        "Как тебя зовут?",
        reply_markup=types.ReplyKeyboardRemove()
    )
    await state.set_state(Register.waiting_name)

# 1. Имя
@router.message(Register.waiting_name)
async def get_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text.strip())
    await message.answer("Когда ты родился(ась)? Напиши в формате ДД.ММ.ГГГГ (например, 15.03.1998)")
    await state.set_state(Register.waiting_birthdate)

# 2. Дата рождения + проверка 18+
@router.message(Register.waiting_birthdate)
async def get_birthdate(message: types.Message, state: FSMContext):
    text = message.text.strip().replace("/", ".").replace("-", ".")
    try:
        birth = datetime.strptime(text, "%d.%m.%Y")
        age = (datetime.now() - birth).days // 365
        await state.update_data(birthdate=text, age=age)

        if age < 18:
            await message.answer(
                "⚠ Внимание!\n\n"
                "Тебе меньше 18 лет.\n"
                "Мы не несем ответственности за участие в играх лиц младше 18 лет.\n"
                "Если ты всё равно хочешь продолжить — напиши «Продолжить»"
            )
            await state.set_state(Register.waiting_under18_confirm)
        else:
            await message.answer("Отлично! Теперь самый интересный вопрос…")
            await ask_fun_fact(message, state)
    except:
        await message.answer("Не поняла дату 😔 Напиши в формате ДД.ММ.ГГГГ (например, 27.12.2001)")

@router.message(Register.waiting_under18_confirm)
async def under18_confirm(message: types.Message, state: FSMContext):
    if message.text.lower() not in ["продолжить", "да", "ок", "ok"]:
        await message.answer("Напиши «Продолжить», если хочешь играть")
        return
    await message.answer("Хорошо, продолжаем! 😏")
    await ask_fun_fact(message, state)

async def ask_fun_fact(message: types.Message, state: FSMContext):
    await message.answer(
        "Факт о тебе, который НИКТО не догадается по твоей внешности или поведению?\n"
        "(например: «Я был(а) в 17 странах», «Я умею играть на скрипке», «У меня 3 кота»)"
    )
    await state.set_state(Register.waiting_fun_fact)

# 3. Факт
@router.message(Register.waiting_fun_fact)
async def get_fun_fact(message: types.Message, state: FSMContext):
    await state.update_data(fun_fact=message.text.strip())
    await message.answer(
        "И последнее — САМАЯ СТРАННАЯ история из твоей жизни?\n"
        "Чем безумнее — тем лучше 😉"
    )
    await state.set_state(Register.waiting_crazy_story)

# 4. Странная история → сохраняем всё
@router.message(Register.waiting_crazy_story)
async def get_crazy_story(message: types.Message, state: FSMContext):
    data = await state.get_data()
    await state.clear()

    await add_user(
        user_id=message.from_user.id,
        name=data["name"],
        birthdate=data["birthdate"],
        age=data.get("age", 0),
        fun_fact=data["fun_fact"],
        crazy_story=message.text.strip()
    )

    await message.answer(
        f"Готово, {data['name']}! 🔥\n\n"
        "Ты в системе. Теперь можно выбирать игры, копить лояльность и ждать безумных вечеров в Варшаве!\n\n"
        "Твоя странная история — это просто 💣",
        reply_markup=main_menu_keyboard()
    )
