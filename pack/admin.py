from django.contrib import admin
from .models import Order, Product, Profile, AppItem, OrderItem, CartItem

# Register the models to appear in the Django admin interface
admin.site.register(Order)
admin.site.register(Product)
admin.site.register(Profile)
admin.site.register(AppItem)
admin.site.register(OrderItem)
admin.site.register(CartItem)
