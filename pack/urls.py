# urls.py
from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from .views import ProductListView, CartListView, OrderListView, UserDetailView

urlpatterns = [
    path('products/', ProductListView.as_view(), name='product-list'),
    path('cart/', CartListView.as_view(), name='cart-list'),
    path('orders/', OrderListView.as_view(), name='order-list'),
    path('api/login/', obtain_auth_token, name='api_token_auth'),  # Login endpoint
    path('api/user/', UserDetailView.as_view(), name='user_detail'),  
]
