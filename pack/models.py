# models.py
from django.contrib.auth.models import User
from django.db import models

CAT = (
    ('rice', 'rice'),
    ('drinks', 'drinks'),
    ('oil', 'oil'),
)

STATUS = (
    ('pending', 'pending'),
    ('confirmed', 'confirmed'),
    ('complete', 'complete'),
)

AVAILABILITY = (
    ('off', 'off'),
    ('on', 'on'),
)

class Product(models.Model):
    name = models.CharField(max_length=25)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    picture = models.ImageField(upload_to='pictures', null=True, blank=True)
    category = models.CharField(choices=CAT, max_length=25)
    availability = models.CharField(choices=AVAILABILITY, max_length=5, default='off')

    def __str__(self):
        return str(self.name)

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cart')
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"Cart of {self.user.username}"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.product.name}"

    @property
    def total_price(self):
        return self.quantity * self.product.price

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    status = models.CharField(choices=STATUS, max_length=25, default='pending')
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order {self.id} by {self.user.username}"

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.TextField(null=True, blank=True)
    phone = models.CharField(max_length=15, null=True, blank=True)
    first_name = models.CharField(max_length=20, blank=True, null=True)
    last_name = models.CharField(max_length=20, blank=True, null=True)
    joined = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['joined']

    def __str__(self):
        return str(self.user)
