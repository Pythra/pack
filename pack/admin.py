from django.contrib import admin
from .models import Order, Product, Profile, AppItem

# Register the models to appear in the Django admin interface
admin.site.register(Order)
admin.site.register(Product)
admin.site.register(Profile)
admin.site.register(AppItem)
