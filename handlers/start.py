# handlers/start.py — ИСПРАВЛЕНО: кнопка "Начать анкету" + регистрация 1 раз + главное меню
from aiogram import Router, F, types
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from database import get_user, add_user
from datetime import datetime

router = Router()

class Register(StatesGroup):
    waiting_name = State()
    waiting_birthdate = State()
    waiting_under18_confirm = State()
    waiting_fun_fact = State()
    waiting_crazy_story = State()

# ГЛАВНОЕ МЕНЮ — РАБОЧЕЕ!
def main_menu(registered: bool = False):
    buttons = [
        [InlineKeyboardButton(text="Игры", callback_data="games")],
        [InlineKeyboardButton(text="Личный кабинет", callback_data="profile")],
        [InlineKeyboardButton(text="Правила", callback_data="show_rules")],
        [InlineKeyboardButton(text="Помощь", callback_data="support_start")],
    ]
    if not registered:
        buttons.insert(0, [InlineKeyboardButton(text="Начать анкету", callback_data="start_registration")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)

# /start — проверяем, зарегистрирован ли уже
@router.message(CommandStart())
async def cmd_start(message: types.Message):
    user = await get_user(message.from_user.id)
    if user and user.get("name") and user.get("birthdate"):
        # УЖЕ ЗАРЕГИСТРИРОВАН — показываем меню
        await message.answer(
            f"С возвращением, {user['name']}! Ты уже в игре!",
            reply_markup=main_menu(registered=True)
        )
    else:
        # ЕЩЁ НЕТ — показываем кнопку "Начать анкету"
        await message.answer(
            "Привет! Я бот для самых крутых игр в Варшаве\n\n"
            "Чтобы участвовать — нужно заполнить анкету (1 раз и навсегда)",
            reply_markup=main_menu(registered=False)
        )

# КНОПКА "Начать анкету"
@router.callback_query(F.data == "start_registration")
async def start_registration(callback: types.CallbackQuery, state: FSMContext):
    user = await get_user(callback.from_user.id)
    if user and user.get("name"):
        await callback.message.edit_text(
            "Ты уже прошёл регистрацию!",
            reply_markup=main_menu(registered=True)
        )
        await callback.answer()
        return

    await state.set_state(Register.waiting_name)
    await callback.message.edit_text("Отлично! Как тебя зовут?")
    await callback.answer()

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
                "Внимание!\n\n"
                "Тебе меньше 18 лет.\n"
                "Мы не несем ответственности за участие в играх лиц младше 18 лет.\n"
                "Если ты всё равно хочешь продолжить — напиши «Продолжить»"
            )
            await state.set_state(Register.waiting_under18_confirm)
        else:
            await message.answer("Отлично! Теперь самый интересный вопрос…")
            await ask_fun_fact(message, state)
    except:
        await message.answer("Не поняла дату Напиши в формате ДД.ММ.ГГГГ (например, 27.12.2001)")

@router.message(Register.waiting_under18_confirm)
async def under18_confirm(message: types.Message, state: FSMContext):
    if message.text.lower() not in ["продолжить", "да", "ок", "ok"]:
        await message.answer("Напиши «Продолжить», если хочешь играть")
        return
    await message.answer("Хорошо, продолжаем!")
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
        "Чем безумнее — тем лучше"
    )
    await state.set_state(Register.waiting_crazy_story)

# 4. Странная история → сохраняем
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
        f"Готово, {data['name']}! Ты в системе!\n\n"
        "Теперь можно выбирать игры и копить лояльность",
        reply_markup=main_menu(registered=True)
    )
