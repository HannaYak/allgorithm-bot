from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from database import get_user

def main_menu():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Мероприятия", callback_data="events")],
        [InlineKeyboardButton(text="Мои записи", callback_data="my_bookings")],
        [InlineKeyboardButton(text="Личный кабинет", callback_data="cabinet")],
        [InlineKeyboardButton(text="Правила", callback_data="rules")],
        [InlineKeyboardButton(text="Помощь", callback_data="support")],
    ])

async def is_registered(callback):
    user = await get_user(callback.from_user.id)
    if not user:
        await callback.answer("Сначала заполни анкету!", show_alert=True)
        return None
    return user
