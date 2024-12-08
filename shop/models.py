import random
import string
from django.db import models
from django.contrib.auth.models import User
import random
import string
from django.db import models

class Coupon(models.Model):
    code = models.CharField(max_length=50, unique=True, blank=True)
    discount = models.DecimalField(max_digits=5, decimal_places=2)
    active = models.BooleanField(default=True)
    expiration_date = models.DateTimeField(null=True, blank=True)

    def generate_coupon_code(self):
        length = 8
        characters = string.ascii_uppercase + string.digits
        return ''.join(random.choice(characters) for _ in range(length))

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = self.generate_coupon_code()
        super().save(*args, **kwargs)

    def is_valid(self):

        if not self.active:
            return False
        if self.expiration_date and self.expiration_date < timezone.now():
            return False
        return True

    def __str__(self):
        return f"{self.code} - {self.discount}%"



class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products', null=True, blank=True)

    def __str__(self):
        return self.name


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="cart", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    coupon = models.ForeignKey(Coupon, on_delete=models.SET_NULL, null=True, blank=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def total(self):
        return sum(item.subtotal() for item in self.items.all())

    def update_total_price(self):
        self.total_price = self.total()
        if self.coupon and self.coupon.active:
            discount = self.coupon.discount / 100
            self.total_price -= (self.total_price * discount)
        self.save()

    def apply_discount(self, coupon):
        if coupon and coupon.active:
            self.coupon = coupon
            self.update_total_price()

    def __str__(self):
        return f"Cart for {self.user.username if self.user else 'Guest'}"




class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def subtotal(self):
        return self.product.price * self.quantity

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"



class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(default=1)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} - {self.rating} звезд'