from django.shortcuts import get_object_or_404
from rest_framework import generics, status 
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.authtoken.models import Token

from .models import Product, AppItem, Order, OrderItem, Profile, CartItem
from .serializers import ProductSerializer, CartItemSerializer, AppItemSerializer, OrderSerializer, OrderItemSerializer, ProfileSerializer, CartItemCreateSerializer, OrderItemCreateSerializer

# View to list all products (authenticated users only)
class ProductListView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

# View to retrieve a single product by its ID
class ProductDetailView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

# View to list all AppItems (public access)
class AppItemListView(generics.ListAPIView):
    queryset = AppItem.objects.all()
    serializer_class = AppItemSerializer
    permission_classes = [AllowAny]


class CartItemListView(generics.ListAPIView):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    permission_classes = [AllowAny] 

class CartItemUpdateView(generics.RetrieveUpdateAPIView):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    permission_classes = [AllowAny]  

class OrderListView(generics.ListAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [AllowAny]  

# List Order Items (public access)
class OrderItemListView(generics.ListAPIView):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    permission_classes = [AllowAny] 

# Create Order Item (public access)
class OrderItemCreateView(generics.CreateAPIView):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemCreateSerializer
    permission_classes = [AllowAny]

# View to retrieve the profile of the authenticated user
class UserDetailView(generics.RetrieveAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get_object(self):
        return get_object_or_404(Profile, user=self.request.user)


class CartItemCreateView(generics.CreateAPIView):
    queryset = OrderItem.objects.all()
    serializer_class = CartItemCreateSerializer
    permission_classes = [AllowAny] 
    
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def fetch_user(request):
    auth_header = request.headers.get('Authorization', '')
    if not auth_header or not auth_header.startswith('Token '):
        return Response({'error': 'Authorization header is improperly formatted'}, status=status.HTTP_400_BAD_REQUEST)

    token = auth_header.split(' ')[1]
    token_obj = Token.objects.filter(key=token).first()

    if not token_obj:
        return Response({'error': 'Invalid token'}, status=status.HTTP_401_UNAUTHORIZED)

    user = token_obj.user
    user_data = {
        'id': user.id,
        'username': user.username,
    }
    return Response(user_data)
 
class CheckoutView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        cart_items = CartItem.objects.filter(user=user)

        # Debugging: Check if there are cart items for the user
        print(f'User: {user.username}, Cart Items Count: {cart_items.count()}')

        if not cart_items.exists():
            return Response({"error": "No items found in the cart."}, status=status.HTTP_404_NOT_FOUND)

        # Calculate total price
        total_price = sum(item.total for item in cart_items)

        # Debugging: Print the total price calculated
        print(f'Total Price Calculated: {total_price}')

        # Create a new order
        order = Order.objects.create(
            user=user,
            status='pending',  
            total=total_price
        )

        # Debugging: Print the order details
        print(f'Order Created: ID {order.id}, User: {user.username}, Total: {total_price}')

        # Create order items from cart items
        for cart_item in cart_items:
            # Debugging: Print details for each cart item
            print(f'Creating Order Item: Product: {cart_item.product}, Quantity: {cart_item.quantity}, Total: {cart_item.total}')
            
            OrderItem.objects.create(
                order=order,
                user=user,
                product=cart_item.product,
                quantity=cart_item.quantity,
                total=cart_item.total,
            )

        # Delete cart items after creating order items
        cart_items.delete()

        # Return response with order ID
        return Response({"order_id": order.id, "message": "Order created successfully."}, status=status.HTTP_201_CREATED)
