from django.db import models
from django.contrib.auth.models import User

from product.models import Product


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.BigIntegerField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    favorites = models.ManyToManyField(Product)

    def __str__(self):
        return self.user.username