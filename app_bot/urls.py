from django.urls import path
from . import views

urlpatterns = [
    path('message-handler/', views.handle_message, name='message_handler')
]
