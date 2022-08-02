from django.db import models
from django.utils import timezone


class TelegramUser(models.Model):
    """
    Таблица зарегестрированных пользователей
    """
    user_id = models.IntegerField(primary_key=True)
    username = models.CharField(max_length=15, null=True)
    first_name = models.CharField(max_length=30)
    phone_num = models.CharField(max_length=30)


class TelegramState(models.Model):
    """
    Таблица актуальных сценариев
    """
    user_id = models.IntegerField(primary_key=True)
    scenario = models.CharField(max_length=30)
    step = models.CharField(max_length=30)
    context = models.JSONField(null=True)


class Feedback(models.Model):
    """
    Таблица отзывов
    """
    user = models.ForeignKey('TelegramUser', on_delete=models.CASCADE)
    feedback = models.CharField(max_length=150)
    created_at = models.DateTimeField(default=timezone.now)
