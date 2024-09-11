from rest_framework import serializers
from .models import Cart, CartItem
from .models import Book

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'price', 'cover_url']

class CartItemSerializer(serializers.ModelSerializer):
    title = serializers.CharField(source='book.title', read_only=True)
    author = serializers.CharField(source='book.author', read_only=True)
    price = serializers.DecimalField(source='book.price', max_digits=10, decimal_places=2, read_only=True)
    cover_url = serializers.CharField(source='book.cover_url', read_only=True)
    id = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = ['id', 'title', 'author', 'price', 'cover_url', 'quantity']

    def get_id(self, obj):
        return obj.book.id

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total_items = serializers.IntegerField(read_only=True)

    class Meta:
        model = Cart
        fields = ['id', 'items', 'total_items']
