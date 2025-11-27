from aiogram import Router, types
from aiogram.filters import CommandStart
from database import get_user
from .common import main_menu

router = Router()

@router.message(CommandStart())
async def cmd_start(message: types.Message):
    user = await get_user(message.from_user.id)
    if user:
        await message.answer(f"С возвращением, {user[1]}! ✨", reply_markup=main_menu())
    else:
        kb = types.InlineKeyboardMarkup(inline_keyboard=[
            [types.InlineKeyboardButton(text="Начать анкету (1 раз и навсегда)", callback_data="start_reg")]
        ])
        await message.answer(
            "Привет! Я бот для самых крутых игр в Варшаве\n\n"
            "Чтобы участвовать — нужно заполнить анкету (1 раз и навсегда)",
            reply_markup=kb
        )
