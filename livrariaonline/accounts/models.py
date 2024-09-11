import uuid
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import AbstractUser
from ..books.models import Cart

class User(AbstractUser):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)


    def my_cart(self):
        card, created = Cart.objects.get_or_create(user=self)
        return card