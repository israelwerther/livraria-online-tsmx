from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Cart, CartItem
from .serializers import CartSerializer, CartItemSerializer, BookSerializer
from .models import Book
from django.shortcuts import get_object_or_404


class CartViewSet(viewsets.ModelViewSet):
    serializer_class = CartSerializer
    queryset = Cart.objects.all()

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Cart.objects.filter(user=self.request.user)
        return Cart.objects.none()

    @action(detail=True, methods=['post'])
    def add_book(self, request, pk=None):
        cart = self.get_object()
        book_id = request.data.get('book_id')
        quantity = request.data.get('quantity', 1)

        book = get_object_or_404(Book, id=book_id)
        cart_item, created = CartItem.objects.get_or_create(cart=cart, book=book)
        if not created:
            cart_item.quantity += quantity
        else:
            cart_item.quantity = quantity

        cart_item.save()

        return Response(data=CartSerializer(instance=cart, many=False).data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'])
    def books_data(self, request, pk=None):
        books_ids = request.data
        return Response(BookSerializer(instance=Book.objects.filter(id__in=books_ids), many=True).data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def remove_book(self, request, pk=None):
        cart = self.get_object()
        book_id = request.data.get('book_id')

        cart_item = get_object_or_404(CartItem, cart=cart, book_id=book_id)
        cart_item.delete()

        return Response(data=CartSerializer(instance=cart, many=False).data, status=status.HTTP_200_OK)



    @action(detail=False, methods=['post'])
    def finalizar_compra(self, request, pk=None):
        data = self.request.data.get('payment_type', 'card')
        user = self.request.user
        cart = user.my_cart()
        cart.finalizar_compra(payment_type=data)

        return Response(status=status.HTTP_200_OK)
