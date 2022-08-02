from django.contrib import admin

from app_cart.models import Cart, CartItem


class CartAdmin(admin.ModelAdmin):
    list_display = ['user', 'created_at']


class CartItemAdmin(admin.ModelAdmin):
    list_display = ['product', 'quantity', 'cart']


admin.site.register(Cart, CartAdmin)
admin.site.register(CartItem, CartItemAdmin)
