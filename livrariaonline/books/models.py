from django.db import models
from django.conf import settings

class Book(models.Model):
    title = models.CharField(max_length=255, null=True, blank=True)
    author = models.CharField(max_length=255, null=True, blank=True)
    first_publish_year = models.IntegerField(null=True, blank=True)
    cover_id = models.IntegerField(null=True, blank=True)
    price = models.DecimalField("Preço", max_digits=8, decimal_places=2, default=100)
    open_library_id = models.CharField(max_length=50, unique=True, null=True, blank=True)
    logged_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.title

    @property
    def cover_url(self):
        if self.cover_id:
            return f'https://covers.openlibrary.org/b/id/{self.cover_id}-L.jpg'
        return None


class Cart(models.Model):
    user = models.OneToOneField("accounts.User", verbose_name=("Usuário"), on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Carrinho - {self.created_at}"
    
    def add_book(self, book_id, quantity):
        CartItem.objects.update_or_create(
            cart=self,
            book=Book.objects.get(id=book_id),
            defaults={
                "quantity": quantity
            }
        )

    def clean_cart(self):
        self.items.all().delete()

    @property
    def total(self):
        return self.items.aggregate(total=models.Sum('book__price')).get('total') or 0
    
    def finalizar_compra(self, payment_type):
        order = Order.objects.create(
            user=self.user
        )
        
        for item in self.items.all():
            order_item = OrderItem.objects.create(
                order=order,
                book=item.book,
                quantity=item.quantity,
            )
        
        self.clean_cart()

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.book.title} ({self.quantity})"
    

class Order(models.Model):
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='orders', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Pedido {self.id} de {self.user.username}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.book.title} ({self.quantity})"



