from django.urls import path
from your_app.consumers import AppItemsConsumer

websocket_urlpatterns = [
    path("ws/app-items/", AppItemsConsumer.as_asgi()),
]
