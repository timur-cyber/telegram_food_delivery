from django.db import models
from django.utils import timezone

from app_bot.models import TelegramUser
from app_products.models import Product


class Cart(models.Model):
    user = models.ForeignKey(TelegramUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)

    @property
    def total_price(self):
        all_items = CartItem.objects.filter(cart=self)
        total = 0
        for item in all_items:
            total += item.product.price * item.quantity
        return total


class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    cart = models.ForeignKey('Cart', on_delete=models.CASCADE)

    @property
    def price_w_quantity(self):
        return self.product.price * self.quantity
