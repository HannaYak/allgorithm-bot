from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from keyboards import main_menu
from database import init
import asyncio

router = Router()

@router.message(Command("start"))
async def cmd_start(message: Message):
    await init()  # создаём базу при первом запуске
    await message.answer(
        "Привет! Добро пожаловать в наш клуб знакомств, общения и интересных встреч.\n\n"
        "Здесь мы создаём пространство, где люди находят друзей, партнёров, единомышленников и просто приятно проводят время.\n\n"
        "У нас три формата мероприятий — от уютных ужинов до быстрых мини-свиданий и интеллектуальных игр.\n\n"
        "Чтобы мы могли подобрать для тебя лучший опыт и корректно бронировать места, давай сначала немного познакомимся.\n"
        "Регистрация проходит один раз и навсегда — всего 5 коротких вопросов, это займёт около минуты.\n\n"
        "Готов начать?",
        reply_markup=main_menu()
    )
