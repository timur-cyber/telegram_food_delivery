from django.contrib import admin

from app_orders.models import Order, OrderItem


class OrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'created_at', 'status']


class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['product', 'quantity', 'order']


admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
