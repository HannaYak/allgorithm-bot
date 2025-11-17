# handlers/profile.py — КАРТА ЛОЯЛЬНОСТИ С ТВОИМИ КАРТИНКАМИ
from aiogram import Router, types, F
from database import get_user
import os

router = Router()

# Путь к папке с картинками
LOYALTY_DIR = "loyalty_images"

@router.message(F.text == "Личный кабинет")
async def profile_with_card(message: types.Message):
    user = await get_user(message.from_user.id)
    
    if not user:
        await message.answer("Ты ещё не прошёл регистрацию! Напиши /start")
        return

    games_played = user.get('games_played', 0)
    loyalty = user.get('loyalty', 0)
    
    # Определяем какую картинку отправлять (от 0 до 5)
    image_number = min(games_played, 10)  # больше 5 — всё равно 5_games.jpg
    image_path = os.path.join(LOYALTY_DIR, f"{image_number}_games.jpg")
    
    # Если файла нет — отправим запасной вариант
    if not os.path.exists(image_path):
        image_path = os.path.join(LOYALTY_DIR, "0_games.jpg")  # дефолтная

    text = (
        f"Личный кабинет\n\n"
        f"Имя: {user.get('name', 'не указано')}\n"
        f"Возраст: {user.get('age', 'не указано')}\n"
        f"Игр сыграно: {games_played}\n"
        f"Лояльность: {loyalty}/5\n\n"
        f"При 5 играх — следующая со скидкой 20%!"
    )

    with open(image_path, "rb") as photo:
        await message.answer_photo(
            photo,
            caption=text,
            parse_mode="HTML"
        )
