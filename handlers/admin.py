from aiogram import Router, F, types
from config import ADMIN_ID

router = Router()

@router.message(F.from_user.id == ADMIN_ID)
async def admin_secret(message: types.Message):
    if message.text == "/admin":
        await message.answer("Админка в разработке. Скоро будет огонь 🔥")
