import json

from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt

from djangoXtelegram.config import TOKEN, NGROK_AUTH_TOKEN
from djangoXtelegram.settings import CSRF_TRUSTED_ORIGINS
from app_bot.engine import BotEngine

from pyngrok import ngrok

bot = BotEngine(TOKEN)
ngrok.set_auth_token(NGROK_AUTH_TOKEN)
http_tunnel = ngrok.connect(8000)
print(http_tunnel)
for tunnel in ngrok.get_tunnels():
    if tunnel.proto == 'https':
        WEBHOOK_URL = tunnel.public_url
        CSRF_TRUSTED_ORIGINS.append(WEBHOOK_URL)
        bot.start_webhook(WEBHOOK_URL)


@csrf_exempt
def handle_message(request: WSGIRequest):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf8'))
        bot.work(data)
    return HttpResponse('Handled successfully')


@csrf_exempt
def complete_order(request: WSGIRequest):
    if request.method == 'POST':
        data = request.POST
        if not data.get('user_id') or not data.get('order_id'):
            return HttpResponseBadRequest('Invalid JSON')
        user_id = data.get('user_id')
        order_id = data.get('order_id')
        bot.bot.send_message(user_id, f'Заказ #{order_id} выполнен')
        return HttpResponse('Completed successfully')


def cancel_order(request: WSGIRequest):
    if request.method == 'POST':
        data = request.POST
        if not data.get('user_id') or not data.get('order_id'):
            return HttpResponseBadRequest('Invalid JSON')
        user_id = data.get('user_id')
        order_id = data.get('order_id')
        bot.bot.send_message(user_id, f'Заказ #{order_id} отменён')
        return HttpResponse('Canceled successfully')
