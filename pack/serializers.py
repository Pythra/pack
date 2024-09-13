from rest_framework import serializers
from .models import Product, AppItem, Order, OrderItem, Profile

# Serializer for Product model
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'picture', 'category', 'description', 'onhand']

# Serializer for AppItem model
class AppItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer()  # Nested product information in the AppItem
    
    class Meta:
        model = AppItem
        fields = ['id', 'saletype', 'creator', 'product', 'displayquantity', 'maxorderquantity', 
                  'minorderquantity', 'condition', 'productratio', 'conditionratio', 'availablecondition', 'created_on']

# Serializer for OrderItem model
class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer()  # Nested product information in the OrderItem
    
    class Meta:
        model = OrderItem
        fields = ['id', 'order', 'product', 'quantity', 'total']

# Serializer for Order model
class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)  # Nested items in the order
    
    class Meta:
        model = Order
        fields = ['id', 'user', 'status', 'total', 'created_on', 'items']

# Serializer for Profile model
class ProfileSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()  # Display username
    
    class Meta:
        model = Profile
        fields = ['user', 'address', 'phone', 'first_name', 'last_name', 'joined']
