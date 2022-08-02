import json

from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from djangoXtelegram.config import TOKEN
from app_bot.engine import BotEngine

bot = BotEngine(TOKEN)


@csrf_exempt
def handle_message(request: WSGIRequest):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf8'))
        bot.work(data)
    return HttpResponse('Handled successfully')
