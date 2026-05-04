from django.db import models

# Create your models here.

class Register(models.Model):
    name=models.CharField(max_length=100)
    email=models.EmailField(unique=True)
    contact=models.IntegerField()
    password=models.CharField(max_length=100)
    city=models.CharField(max_length=200)

    def __str__(self):
        return self.name
    
class Product(models.Model):
    CATEGORY_CHOICE = (
        ('vegetable', 'Vegetable'),
        ('fruit', 'Fruit'),
    )

    image = models.ImageField(upload_to='products/')
    name = models.CharField(max_length=100)
    descriptions = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICE,
        default='fruit'
    )

    def __str__(self):
        return self.name
    
class Cart(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
 
    def __str__(self):
        return self.product.name
    
class Checkout(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    companyname = models.CharField(max_length=100, blank=True)
    address = models.TextField()
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10)
    mobile = models.CharField(max_length=15)
    email = models.EmailField()
    create_account = models.BooleanField(default=False)
    ship_to_different_address = models.BooleanField(default=False)
    order_notes = models.TextField(blank=True)

    def __str__(self):
        return self.first_name
    
class OrderItem(models.Model):
    checkout = models.ForeignKey(Checkout, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.FloatField()
 
    def __str__(self):
        return f"{self.product.name} x {self.quantity}"