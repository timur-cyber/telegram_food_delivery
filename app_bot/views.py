import json

from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from djangoXtelegram.config import TOKEN
from djangoXtelegram.settings import CSRF_TRUSTED_ORIGINS
from app_bot.engine import BotEngine

from pyngrok import ngrok

bot = BotEngine(TOKEN)
ngrok.set_auth_token("2BZeOzGWedONZFAMFzl2rkfMD4a_4AEWxNKLMn1zQ5NHpvZa5")
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
