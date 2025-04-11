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
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='icecream_images/', null=True, blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return self.name