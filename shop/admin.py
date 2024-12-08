from django.contrib import admin
from .models import Product, Category, Coupon

admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Coupon)

# Register your models here.
