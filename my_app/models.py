from django.db import models
class Contact(models.Model):
    name = models.CharField(max_length=150)
    phone =models.CharField(max_length=10) 
    email = models.EmailField(max_length=100)
    desc = models.TextField(max_length=500)
    date = models.DateField()
# Create your models here.
