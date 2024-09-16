from django.urls import reverse
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from .models import Product, OrderItem
from django.contrib.auth.models import User

class ProductTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('products')  # Updated to match the URL pattern name

    def test_create_product(self):
        response = self.client.post(self.url, {'name': 'Test Product', 'price': 10.00}, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Product.objects.count(), 1)
        self.assertEqual(Product.objects.get().name, 'Test Product')

    def test_delete_product(self):
        # Setup initial product
        product = Product.objects.create(name='Test Product', price=10.00)
        response = self.client.delete(reverse('product-detail', args=[product.id]))  # Ensure 'product-detail' exists
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Product.objects.count(), 0)

    def test_get_products(self):
        Product.objects.create(name='Test Product', price=10.00)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_update_product(self):
        product = Product.objects.create(name='Test Product', price=10.00)
        response = self.client.put(reverse('product-detail', args=[product.id]), {'name': 'Updated Product', 'price': 15.00}, format='json')  # Ensure 'product-detail' exists
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Product.objects.get().name, 'Updated Product')

class UserAuthenticationTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.username = 'testuser'
        self.password = 'testpassword'
        # Create a user
        self.user = User.objects.create_user(username=self.username, password=self.password)

    def test_login(self):
        response = self.client.post(reverse('login'), {'username': self.username, 'password': self.password}, format='json')  # Ensure 'login' exists
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)

    def test_login_failure(self):
        response = self.client.post(reverse('login'), {'username': 'wronguser', 'password': 'wrongpassword'}, format='json')  # Ensure 'login' exists
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_access_protected_view(self):
        # First, login to obtain the token
        login_response = self.client.post(reverse('login'), {'username': self.username, 'password': self.password}, format='json')  # Ensure 'login' exists
        token = login_response.data['token']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        response = self.client.get(reverse('protected-view'))  # Ensure 'protected-view' exists
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_access_protected_view_without_token(self):
        response = self.client.get(reverse('protected-view'))  # Ensure 'protected-view' exists
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
