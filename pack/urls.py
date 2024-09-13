from django.urls import path
from . import views

urlpatterns = [
    # Route for listing products
    path('products/', views.ProductListView.as_view(), name='product-list'),

    # Route for listing AppItems
    path('app-items/', views.AppItemListView.as_view(), name='app-item-list'),

    # Route for listing orders of the authenticated user
    path('orders/', views.OrderListView.as_view(), name='order-list'),

    # Route for retrieving user profile
    path('user/profile/', views.UserDetailView.as_view(), name='user-profile'),
]
