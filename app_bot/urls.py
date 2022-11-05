from django.urls import path
from . import views

urlpatterns = [
    path('message-handler/', views.handle_message, name='message_handler'),
    path('complete-order/', views.complete_order, name='complete_order'),
    path('cancel-order/', views.cancel_order, name='cancel-order'),
]
