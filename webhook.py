async def handle_success_payment(session):
    user_id = int(session['client_reference_id'])
    payment_id = session['metadata']['payment_id']
    game_key = session['metadata']['game']

    # Обновляем статус
    await db.update_payment_status(payment_id, "completed")

    # Добавляем игру в профиль
    await db.increment_games_played(user_id)

    # Сообщение
    game_name = {
        "meet_eat": "Meet&Eat",
        "lock_stock": "Лок Сток",
        "bar_liar": "Бар Лжецов",
        "speed_dating": "Быстрые Свидания"
    }[game_key]

    await bot.send_message(
        user_id,
        f"Оплата прошла!\n\n"
        f"Ты записан на: *{game_name}*\n"
        f"Дата: {datetime.datetime.now().strftime('%d.%m %H:%M')}\n\n"
        f"Спасибо! Ждём тебя в Варшаве",
        parse_mode="Markdown"
    )
