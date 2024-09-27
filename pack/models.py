from django.contrib.auth.models import User
from django.db import models

CAT = (
    ('rice', 'rice'),
    ('drinks', 'drinks'),
    ('oil', 'oil'),
)

STATUS = (
    ('empty', 'empty'),
    ('unplaced', 'unplaced'),
    ('pending', 'pending'),
    ('confirmed', 'confirmed'),
    ('complete', 'complete'),
)

SALETYPE = (
    ('normal', 'normal'),
    ('preorder', 'preorder'),
    ('bulkbuy', 'bulkbuy'),
    ('subdistribution', 'subdistribution'),
    ('paysmall', 'paysmall'),
)

class Product(models.Model):
    name = models.CharField(max_length=25)
    forsale = models.BooleanField(default=False)
    price = models.IntegerField()
    picture = models.ImageField(upload_to='pictures', null=True, blank=True)
    category = models.CharField(choices=CAT, max_length=25, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    onhand = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name

class AppItem(models.Model):
    saletype = models.CharField(choices=SALETYPE, max_length=25, default='normal')
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    displayquantity = models.PositiveIntegerField(default=0)
    maxorderquantity = models.IntegerField(default=50)
    minorderquantity = models.IntegerField(default=1)
    condition = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True, related_name='conditioned_items')
    productratio = models.IntegerField(default=10)
    conditionratio = models.IntegerField(default=1)
    availablecondition = models.PositiveIntegerField( null=True, blank=True, )
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product.name} - {self.saletype}"

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(choices=STATUS, max_length=25, default='pending')
    total = models.PositiveIntegerField(default=0)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id} by {self.user.username}"

class OrderItem(models.Model): 
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items', blank=True, null=True)  # Link to Order
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)    
    session_id = models.CharField(max_length=100, null=True, blank=True)  # Temporary identifier
    total = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.quantity} of {self.product.name}"

 
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.TextField(null=True, blank=True)
    phone = models.CharField(max_length=15, null=True, blank=True)
    first_name = models.CharField(max_length=20, blank=True, null=True)
    last_name = models.CharField(max_length=20, blank=True, null=True)
    joined = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['joined']

    def __str__(self):
        return str(self.user)
