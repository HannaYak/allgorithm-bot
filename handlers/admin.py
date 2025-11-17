from aiogram import Router, types
from aiogram.filters import Command
from config import ADMIN_ID
from database import db

router = Router()

@router.message(Command("admin"))
async def admin_panel(message: types.Message):
    if message.from_user.id != ADMIN_ID:
        await message.answer("Доступ запрещён.")
        return
    
    stats = await db.get_stats()
    text = (
        f"Админ-панель\n\n"
        f"Пользователей: {stats['users']}\n"
        f"Оплат: {stats['payments']}\n"
        f"Игр: {stats['games']}\n\n"
        f"Команды:\n"
        f"/stats — статистика\n"
        f"/broadcast — рассылка"
    )
    
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text="Управлять играми", callback_data="manage_games")],
        [types.InlineKeyboardButton(text="Выйти", callback_data="back_to_start")]
    ])
    
    await message.answer(text, reply_markup=keyboard)
