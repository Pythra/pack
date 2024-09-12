from django.contrib import admin
from .models import Order, Product, Profile, Cart, CartItem

admin.site.register(Order)
admin.site.register(Product)
admin.site.register(Profile)
admin.site.register(Cart)
admin.site.register(CartItem)
