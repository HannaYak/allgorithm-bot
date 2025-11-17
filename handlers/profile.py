# handlers/profile.py — ЛИЧНЫЙ КАБИНЕТ РАБОТАЕТ НАВСЕГДА
from aiogram import Router, types, F
from database import get_user
import os

router = Router()

@router.message(F.text == "Личный кабинет")
async def profile_with_card(message: types.Message):
    user = await get_user(message.from_user.id)
    
    if not user:
        await message.answer("Ты ещё не прошёл регистрацию! Напиши /start")
        return

    # Защита от None
    name = user.get("name") or "не указано"
    age = user.get("age") or "не указано"
    games_played = user.get("games_played") or 0
    loyalty = user.get("loyalty") or 0

    # Карта лояльности (если папка и картинки есть)
    image_number = min(games_played, 5)
    image_path = f"loyalty_images/{image_number}_games.jpg"
    
    text = (
        f"Личный кабинет\n\n"
        f"Имя: {name}\n"
        f"Возраст: {age}\n"
        f"Игр сыграно: {games_played}\n"
        f"Лояльность: {loyalty}/5\n\n"
        f"При 5 играх — следующая со скидкой 20%!"
    )

    # Если картинка есть — отправляем с ней, если нет — просто текст
    if os.path.exists(image_path):
        with open(image_path, "rb") as photo:
            await message.answer_photo(photo, caption=text)
    else:
        await message.answer(text)
