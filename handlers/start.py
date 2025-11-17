from aiogram import Router, types
from aiogram.filters import CommandStart
from config import bot

router = Router()

@router.message(CommandStart())
async def cmd_start(message: types.Message):
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text="Игры", callback_data="show_games")],
        [types.InlineKeyboardButton(text="Личный кабинет", callback_data="profile")],
        [types.InlineKeyboardButton(text="Помощь", callback_data="help")]
    ])
    await message.answer(
        "Привет! Это бот для игр в Варшаве\n\n"
        "Выбери, что хочешь:",
        reply_markup=keyboard
    )
