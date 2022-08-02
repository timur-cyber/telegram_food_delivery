from django.db import models


class Category(models.Model):
    category_name = models.CharField(max_length=30)

    def __str__(self):
        return self.category_name


class Product(models.Model):
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=150)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    price = models.PositiveIntegerField()
    image = models.ImageField(default='nomedia.png')

    def __str__(self):
        return self.name
