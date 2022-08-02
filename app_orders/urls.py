from django.urls import path
from . import views

urlpatterns = [
    path('', views.AllOrdersView.as_view(), name='all_orders'),
    path('active/', views.ActiveOrdersView.as_view(), name='active_orders'),
    path('finished/', views.FinishedOrdersView.as_view(), name='finished_orders'),
    path('canceled/', views.CanceledOrdersView.as_view(), name='canceled_orders'),
    path('<int:id>/', views.OneOrderView.as_view(), name='products_list'),
    path('finish-order/<int:id>', views.finish_order, name='finish_order'),
    path('cancel-order/<int:id>', views.cancel_order, name='finish_order')
]
