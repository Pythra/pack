from django.test import TestCase
from django.contrib.auth.models import User
from .models import Product, Order, AppItem, Profile

class ProductModelTest(TestCase):
    def setUp(self):
        # Create a sample product
        self.product = Product.objects.create(
            name='Sample Rice',
            price=1000,
            category='rice',
            description='High-quality rice',
            onhand=10
        )

    def test_product_creation(self):
        # Test that the product was created successfully
        self.assertEqual(self.product.name, 'Sample Rice')
        self.assertEqual(self.product.price, 1000)
        self.assertEqual(self.product.onhand, 10)

    def test_product_str_representation(self):
        # Test the string representation of the product
        self.assertEqual(str(self.product), 'Sample Rice')

class OrderModelTest(TestCase):
    def setUp(self):
        # Create a user
        self.user = User.objects.create_user(username='testuser', password='12345')
        # Create an order
        self.order = Order.objects.create(
            user=self.user,
            status='pending',
            total=5000
        )

    def test_order_creation(self):
        # Test that the order was created successfully
        self.assertEqual(self.order.user.username, 'testuser')
        self.assertEqual(self.order.total, 5000)

    def test_order_str_representation(self):
        # Test the string representation of the order
        self.assertEqual(str(self.order), f"Order {self.order.id} by testuser")

class ProfileModelTest(TestCase):
    def setUp(self):
        # Create a user
        self.user = User.objects.create_user(username='testuser', password='12345')
        # Create a profile for the user
        self.profile = Profile.objects.create(
            user=self.user,
            phone='1234567890'
        )

    def test_profile_creation(self):
        # Test that the profile was created successfully
        self.assertEqual(self.profile.user.username, 'testuser')
        self.assertEqual(self.profile.phone, '1234567890')

    def test_profile_str_representation(self):
        # Test the string representation of the profile
        self.assertEqual(str(self.profile), 'testuser')
