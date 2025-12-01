from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

router = Router()

# Кнопка для начала анкеты
def get_start_kb():
    kb = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text="Начать анкету")]
    ], resize_keyboard=True)
    return kb

# Главное меню после регистрации
def main_menu():
    kb = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text="Игры"), KeyboardButton(text="Мероприятия")],
        [KeyboardButton(text="Личный кабинет"), KeyboardButton(text="Помощь")]
    ], resize_keyboard=True)
    return kb

@router.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer(
        "Привет! Добро пожаловать в наш клуб знакомств, общения и интересных встреч.\n\n"
        "Здесь мы создаём пространство, где люди находят друзей, партнёров, единомышленников и просто приятно проводят время.\n\n"
        "У нас три формата мероприятий — от уютных ужинов до быстрых мини-свиданий и интеллектуальных игр.\n\n"
        "Чтобы мы могли подобрать для тебя лучший опыт и корректно бронировать места, давай сначала немного познакомимся.\n"
        "Регистрация проходит один раз и навсегда — всего 5 коротких вопросов, это займёт около минуты.\n\n"
        "Готов начать?",
        reply_markup=get_start_kb()
    )
