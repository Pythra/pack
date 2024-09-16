from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from .views import (ProductListView, ProductDetailView,AppItemListView, OrderItemListView, 
                    OrderListView, UserDetailView, OrderItemCreateView, fetch_user
)

urlpatterns = [
    path('products/', ProductListView.as_view(), name='products'),
    path('app-items/', AppItemListView.as_view(), name='app-items'),
    path('order-items/', OrderItemListView.as_view(), name='order-items'),
    path('orders/', OrderListView.as_view(), name='orders'),
    path('profile/', UserDetailView.as_view(), name='profile'),
    path('order-items/create/', OrderItemCreateView.as_view(), name='orderitem-create'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
    path('login/', obtain_auth_token, name='login'), 
    path('user/', fetch_user, name='fetch-user'),

]
