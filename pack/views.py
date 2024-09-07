from rest_framework import generics
from .models import Product, Order, Profile
from .serializers import ProductSerializer, OrderSerializer, ProfileSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

class ProductListView(APIView):
    permission_classes = [AllowAny]  # Allow all users, no authentication required

    def get(self, request, format=None):
        products = Product.objects.all()  # Fetch all products
        serializer = ProductSerializer(products, many=True)  # Serialize the data
        return Response(serializer.data)  
