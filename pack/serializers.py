from rest_framework import serializers
from .models import Product, Order, Profile, AppItem, OrderItem, CartItem

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'forsale', 'price', 'picture', 'category', 'description', 'onhand']

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'user', 'status', 'total', 'created_on']

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['user', 'address', 'phone', 'first_name', 'last_name', 'joined']

class AppItemSerializer(serializers.ModelSerializer):    
    product = ProductSerializer()
    condition = ProductSerializer()
    
    class Meta:
        model = AppItem
        fields = ['id', 'saletype', 'creator', 'product', 'displayquantity', 'maxorderquantity', 'minorderquantity', 'condition', 'productratio', 'conditionratio', 'availablecondition', 'created_on']

class OrderItemSerializer(serializers.ModelSerializer):  
    product = ProductSerializer()
    
    class Meta:
        model = OrderItem
        fields = ['order', 'user', 'product', 'quantity', 'total']

class OrderItemCreateSerializer(serializers.ModelSerializer):  
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())
    
    class Meta:
        model = OrderItem
        fields = ['order', 'user', 'product', 'quantity', 'total']
 
class CartItemCreateSerializer(serializers.ModelSerializer):  
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())
    
    class Meta:
        model = CartItem
        fields = ['user', 'session_id', 'product', 'quantity', 'total']
     
class CartItemSerializer(serializers.ModelSerializer):  
    product = ProductSerializer()
    
    class Meta:
        model = CartItem
        fields = ['user', 'session_id', 'product', 'quantity', 'total']