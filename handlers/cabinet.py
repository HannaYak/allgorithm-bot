from aiogram import Router, types
from database import get_user
from .common import is_registered

router = Router()

@router.callback_query(lambda c: c.data == "cabinet")
async def cabinet(callback: types.CallbackQuery):
    user = await is_registered(callback)
    if not user: return

    await callback.message.edit_text(
        f"Личный кабинет\n\n"
        f"Имя: {user[1]}\n"
        f"Возраст: {user[3]}\n"
        f"Факт: {user[4]}\n"
        f"История: {user[5][:100]}...\n",
        reply_markup=types.InlineKeyboardMarkup(inline_keyboard=[
            [types.InlineKeyboardButton(text="Назад", callback_data="back_main")]
        ])
    )
