from django.db import models
from django.contrib.auth.models import User
class Contact(models.Model):
    name = models.CharField(max_length=150)
    phone =models.CharField(max_length=10) 
    email = models.EmailField(max_length=100)
    desc = models.TextField(max_length=500)
    date = models.DateField()
    
    def __str__(self):
        return self.name # to define name in admin 
class Icecream(models.Model):
    CATEGORY_CHOICES = [
        ('Icecream', 'Icecream'),
        ('Softy', 'Softy'),
        ('Milkshake', 'Milkshake'),
    ]
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='icecream_images/', null=True, blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    added_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    category = models.CharField(max_length=100, choices=CATEGORY_CHOICES)
    def __str__(self):
        return self.name
    
class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    icecream = models.ForeignKey('Icecream', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def subtotal(self):
        return self.quantity * self.icecream.price 

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    address = models.TextField()
    total_amount = models.FloatField()

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    icecream = models.ForeignKey('Icecream', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.FloatField()
    @property
    def total_price(self):
        return self.quantity * self.price