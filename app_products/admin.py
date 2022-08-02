from django.contrib import admin

from app_products.models import Category, Product


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['category_name']


class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'category', 'price', 'image']


admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
