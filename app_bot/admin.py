from django.contrib import admin

from app_bot.models import TelegramUser, TelegramState, Feedback


class TelegramUserAdmin(admin.ModelAdmin):
    list_display = ['user_id', 'username', 'first_name', 'phone_num']


class TelegramStateAdmin(admin.ModelAdmin):
    list_display = ['user_id', 'scenario', 'step']


class FeedbackAdmin(admin.ModelAdmin):
    list_display = ['user', 'feedback', 'created_at']


admin.site.register(TelegramUser, TelegramUserAdmin)
admin.site.register(TelegramState, TelegramStateAdmin)
admin.site.register(Feedback, FeedbackAdmin)
