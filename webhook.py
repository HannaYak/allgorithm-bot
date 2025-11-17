from flask import Flask, request, abort
from config import dp, bot, STRIPE_WEBHOOK_SECRET
import stripe
import asyncio

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def stripe_webhook():
    payload = request.data
    sig_header = request.headers.get('Stripe-Signature')

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, STRIPE_WEBHOOK_SECRET
        )
    except ValueError:
        return abort(400)
    except stripe.error.SignatureVerificationError:
        return abort(400)

    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        user_id = session['client_reference_id']
        asyncio.create_task(handle_success_payment(user_id))

    return '', 200

async def handle_success_payment(user_id):
    await bot.send_message(user_id, "Оплата прошла! Вы записаны на игру!")

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    print(f"Webhook server running on port {port}")
    app.run(host='0.0.0.0', port=port)
