from django.db import models
from django.utils import timezone

from app_bot.models import TelegramUser
from app_products.models import Product

STATUS_CHOICE = (
    ("Активный", "Активный"),
    ("Выполнен", "Выполнен"),
    ("Отменён", "Отменён")
)


class Order(models.Model):
    user = models.ForeignKey(TelegramUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    address = models.CharField(max_length=100)
    status = models.CharField(max_length=30, choices=STATUS_CHOICE, default="Активный")

    @property
    def total_price(self):
        all_items = OrderItem.objects.filter(order_id=self.id)
        total = 0
        for item in all_items:
            total += item.product.price * item.quantity
        return total

    @property
    def formatted_date(self):
        date = Order.objects.get(id=self.id).created_at
        return date.strftime("%d.%m.%Y | %H:%M")


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    order = models.ForeignKey('Order', on_delete=models.CASCADE)

    @property
    def price_w_quantity(self):
        return self.product.price * self.quantity
