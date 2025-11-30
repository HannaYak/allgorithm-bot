from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

def main_menu():
    kb = [
        [KeyboardButton(text="Игры"), KeyboardButton(text="Мероприятия")],
        [KeyboardButton(text="Личный кабинет"), KeyboardButton(text="Помощь")]
    ]
    return ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)

def games_menu():
    kb = [
        [KeyboardButton(text="Talk & Toast")],
        [KeyboardButton(text="Stock & Know")],
        [KeyboardButton(text="Быстрые свидания")],
        [KeyboardButton(text="Назад в меню")]
    ]
    return ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
