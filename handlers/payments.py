from aiogram import Router, types
from config import bot, STRIPE_SECRET_KEY
import stripe
import uuid
from database import get_user, add_user, get_stats, init_db
import datetime

router = Router()
stripe.api_key = STRIPE_SECRET_KEY

# === СОЗДАНИЕ ОПЛАТЫ ===
@router.callback_query(lambda c: c.data.startswith("pay:"))
async def create_payment(callback: types.CallbackQuery):
    game_key = callback.data.split(":")[1]
    game = {
        "meet_eat": ("Meet&Eat", 50),
        "lock_stock": ("Лок Сток", 60),
        "bar_liar": ("Бар Лжецов", 55),
        "speed_dating": ("Быстрые Свидания", 70)
    }[game_key]

    # Генерируем уникальный ID
    payment_id = str(uuid.uuid4())

    try:
        session = stripe.checkout.Session.create(
            payment_method_types=['card', 'blik', 'p24'],
            line_items=[{
                'price_data': {
                    'currency': 'pln',
                    'product_data': {'name': f"{game[0]} — запись на игру"},
                    'unit_amount': game[1] * 100,
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url=f"https://t.me/{(await bot.get_me()).username}?start=paid_{payment_id}",
            cancel_url=f"https://t.me/{(await bot.get_me()).username}?start=cancel",
            client_reference_id=str(callback.from_user.id),
            metadata={'game': game_key, 'payment_id': payment_id}
        )

        # Сохраняем в БД
        await db.add_payment(
            user_id=callback.from_user.id,
            payment_id=payment_id,
            game=game_key,
            amount=game[1],
            status="pending"
        )

        keyboard = types.InlineKeyboardMarkup(inline_keyboard=[
            [types.InlineKeyboardButton(text="Оплатить Blik / Карта / P24", url=session.url)],
            [types.InlineKeyboardButton(text="Отмена", callback_data="show_games")]
        ])

        await callback.message.edit_text(
            f"Оплата за игру\n\n"
            f"Игра: *{game[0]}*\n"
            f"Сумма: {game[1]} PLN\n\n"
            f"Выбери способ оплаты:",
            reply_markup=keyboard,
            parse_mode="Markdown"
        )

    except Exception as e:
        await callback.message.edit_text(f"Ошибка оплаты: {str(e)}")
