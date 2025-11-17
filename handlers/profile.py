# handlers/profile.py — ФИНАЛЬНАЯ ВЕРСИЯ
from aiogram import Router, types, F
from database import get_user, add_user

router = Router()  # ← ЭТО САМОЕ ГЛАВНОЕ! ДОЛЖЕН БЫТЬ router!!!

@router.message(F.text == "Личный кабинет")
async def profile_from_menu(message: types.Message):
    from handlers.profile import show_profile  # если у тебя есть функция
    # Или просто:
    await message.answer("Личный кабинет в разработке — скоро будет!")

@router.callback_query(F.data == "profile")
async def show_profile(callback: types.CallbackQuery):
    user = await get_user(callback.from_user.id)
    
    if not user:
        # Если пользователя нет в БД — создаём
        await add_user(callback.from_user.id)
        user = {"name": "не указано", "age": None, "games_played": 0, "loyalty": 0}

    text = (
        f"Личный кабинет\n\n"
        f"Имя: {user.get('name', 'не указано')}\n"
        f"Возраст: {user.get('age', 'не указано')}\n"
        f"Игр сыграно: {user.get('games_played', 0)}\n"
        f"Лояльность: {user.get('loyalty', 0)}/5 ⭐\n\n"
        f"При 5 играх — следующая со скидкой 20%!"
    )
    
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text="Обновить имя", callback_data="edit_name")],
        [types.InlineKeyboardButton(text="Обновить возраст", callback_data="edit_age")],
        [types.InlineKeyboardButton(text="Назад в меню", callback_data="back_to_start")]
    ])
    
    await callback.message.edit_text(text, reply_markup=keyboard)

# Простые редакторы (можно потом расширить через FSM)
@router.callback_query(F.data == "edit_name")
async def edit_name(callback: types.CallbackQuery):
    await callback.message.edit_text("Пришли своё имя:")
    # Здесь можно добавить FSM, но пока просто скажем, что будет дальше
    await callback.answer("Функция в разработке — скоро будет!")

@router.callback_query(F.data == "edit_age")
async def edit_age(callback: types.CallbackQuery):
    await callback.message.edit_text("Пришли свой возраст:")
    await callback.answer("Функция в разработке — скоро будет!")
