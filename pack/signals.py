# your_app/signals.py

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Order

@receiver(post_save, sender=User)
def create_order_for_new_user(sender, instance, created, **kwargs):
    if created:
        Order.objects.create(user=instance)
