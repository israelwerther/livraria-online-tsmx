from django.contrib import admin
from .models import Cart, CartItem, Book, Order, OrderItem

admin.site.register([Book, Cart, CartItem, Order, OrderItem])