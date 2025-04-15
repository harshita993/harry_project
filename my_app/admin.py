from django.contrib import admin
from my_app.models import Contact,Icecream, CartItem,Order, OrderItem

admin.site.register(Icecream)
admin.site.register(Contact)
admin.site.register(CartItem)
admin.site.register(Order)
admin.site.register(OrderItem)
# Register your models here.
