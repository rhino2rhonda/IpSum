from django.contrib import admin
from products.models import Product
from shops.models import ProductOffer

# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'product_category', 'product_type', 'mrp')

admin.site.register(Product, ProductAdmin)
