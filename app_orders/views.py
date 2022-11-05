from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from django.test import Client

from app_orders.models import Order, OrderItem

client = Client()

class AllOrdersView(View):
    def get(self, request):
        if not request.user.is_staff:
            return HttpResponse('Not allowed', 401)
        orders = sorted(Order.objects.all(), key=lambda x: x.created_at, reverse=True)
        return render(request, 'orders_widget.html', context={'orders': orders})


class ActiveOrdersView(View):
    def get(self, request):
        if not request.user.is_staff:
            return HttpResponse('Not allowed', 401)
        orders = Order.objects.filter(status='Активный')
        orders = sorted(orders, key=lambda x: x.created_at, reverse=True)
        return render(request, 'orders_widget.html', context={'orders': orders})


class FinishedOrdersView(View):
    def get(self, request):
        if not request.user.is_staff:
            return HttpResponse('Not allowed', 401)
        orders = Order.objects.filter(status='Выполнен')
        orders = sorted(orders, key=lambda x: x.created_at, reverse=True)
        return render(request, 'orders_widget.html', context={'orders': orders})


class CanceledOrdersView(View):
    def get(self, request):
        if not request.user.is_staff:
            return HttpResponse('Not allowed', 401)
        orders = Order.objects.filter(status='Отменён')
        orders = sorted(orders, key=lambda x: x.created_at, reverse=True)
        return render(request, 'orders_widget.html', context={'orders': orders})


class OneOrderView(View):
    def get(self, request, id):
        if not request.user.is_staff:
            return HttpResponse('Not allowed', 401)
        order = Order.objects.get(id=id)
        order_items = OrderItem.objects.filter(order=order)
        return render(request, 'one_order.html',
                      context={'order': order, 'order_items': order_items})


def finish_order(request, id):
    if not request.user.is_staff:
        return HttpResponse('Not allowed', 401)
    order = Order.objects.get(id=id)
    order.status = 'Выполнен'
    order.save()
    user_id = order.user.user_id
    client.post('/bot/complete-order/', {'user_id': user_id, 'order_id': id})
    return redirect(request.META.get('HTTP_REFERER') or '/')


def cancel_order(request, id):
    if not request.user.is_staff:
        return HttpResponse('Not allowed', 401)
    order = Order.objects.get(id=id)
    order.status = 'Отменён'
    order.save()
    user_id = order.user.user_id
    client.post('/bot/cancel-order/', {'user_id': user_id, 'order_id': id})
    return redirect(request.META.get('HTTP_REFERER') or '/')
