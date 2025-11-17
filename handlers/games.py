from aiogram import Router, types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from database import db
import datetime

router = Router()

class OrderGame(StatesGroup):
    choosing_game = State()
    confirming = State()

GAMES = {
    "meet_eat": {"name": "Meet&Eat", "price": 50, "emoji": "Ресторан"},
    "lock_stock": {"name": "Лок Сток", "price": 60, "emoji": "Замок"},
    "bar_liar": {"name": "Бар Лжецов", "price": 55, "emoji": "Кож"},
    "speed_dating": {"name": "Быстрые Свидания", "price": 70, "emoji": "Сердце"}
}

@router.callback_query(lambda c: c.data == "show_games")
async def show_games(callback: types.CallbackQuery, state: FSMContext):
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(
            text=f"{g['emoji']} {g['name']} — {g['price']} PLN",
            callback_data=f"select_game:{key}"
        )] for key, g in GAMES.items()
    ] + [[types.InlineKeyboardButton(text="Назад", callback_data="back_to_start")]])
    
    await callback.message.edit_text("Выбери игру:", reply_markup=keyboard)
    await state.set_state(OrderGame.choosing_game)

@router.callback_query(lambda c: c.data.startswith("select_game:"))
async def select_game(callback: types.CallbackQuery, state: FSMContext):
    game_key = callback.data.split(":")[1]
    game = GAMES[game_key]
    
    await state.update_data(game=game_key, price=game["price"])
    
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text="Оплатить", callback_data=f"pay:{game_key}")],
        [types.InlineKeyboardButton(text="Назад", callback_data="show_games")]
    ])
    
    await callback.message.edit_text(
        f"Игра: *{game['name']}*\n"
        f"Цена: {game['price']} PLN\n\n"
        "Готов оплатить?",
        reply_markup=keyboard,
        parse_mode="Markdown"
    )
