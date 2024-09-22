from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework.decorators import api_view, permission_classes
from rest_framework.authtoken.models import Token

from .models import Product, AppItem, Order, OrderItem, Profile
from .serializers import ProductSerializer, AppItemSerializer, OrderSerializer, OrderItemSerializer, ProfileSerializer, OrderItemCreateSerializer

# View to list all products (authenticated users only)
class ProductListView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

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
    permission_classes = [AllowAny]  # Public access allowed


class OrderItemListView(generics.ListAPIView):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    permission_classes = [AllowAny] 
    
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
    
     

@api_view(['GET'])
def fetch_user(request):
    try:
        auth_header = request.headers.get('Authorization', '')
        
        # Check if the header is present and properly formatted
        if not auth_header or not auth_header.startswith('Token '):
            return Response({'error': 'Authorization header is improperly formatted'}, status=400)

        # Extract the token
        token = auth_header.split(' ')[1]

        try:
            token_obj = Token.objects.get(key=token)
            user = token_obj.user
        except Token.DoesNotExist:
            return Response({'error': 'Invalid token'}, status=401)

        user_data = {
            'id': user.id,
            'username': user.username,
        }
        return Response(user_data)
    
    except IndexError:
        return Response({'error': 'Authorization header is improperly formatted'}, status=400)
    except Exception as e:
        return Response({'error': str(e)}, status=500)
    
@api_view(['POST'])
def transfer_order_items(request):
    user = request.user
    session_id = request.data.get('session_id')

    # Transfer all OrderItems with session_id to the logged-in user
    order_items = OrderItem.objects.filter(session_id=session_id)
    order_items.update(user=user, session_id=None)

    return Response({'status': 'success', 'message': 'Order items transferred successfully'})

@api_view(['POST'])
def checkout(request):
    user = request.user if request.user.is_authenticated else None
    session_id = request.data.get('session_id')
    
    if not user and not session_id:
        return Response({"error": "User or session ID is required."}, status=status.HTTP_400_BAD_REQUEST)

    # Fetch all OrderItems for the user or session_id
    if user:
        order_items = OrderItem.objects.filter(user=user)
    else:
        order_items = OrderItem.objects.filter(session_id=session_id)

    if not order_items.exists():
        return Response({"error": "No items found in the cart."}, status=status.HTTP_404_NOT_FOUND)

    # Calculate the total price of all the items in the cart
    total_price = sum(item.total for item in order_items)

    # Create a new Order for the user with a default status of 'unplaced'
    order = Order.objects.create(
        user=user,
        status='unplaced',  # Default status for newly created orders
        total=total_price
    )

    # Update OrderItems to associate them with the newly created Order
    order_items.update(user=user)  # Assign the user if session_id was used earlier

    # Optionally, delete all the OrderItems to clear the cart
    order_items.delete()

    return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)