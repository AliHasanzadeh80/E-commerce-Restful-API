from django.db import models

from django.contrib.auth.models import User
from product.models import Product, Additional_choice_values


class Cart(models.Model):
    status_choices = (
        ('in-process', 'in-process'),
        ('delivered', 'delivered')
    )
    customer = models.OneToOneField(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, choices=status_choices, default='in-process')

    def __str__(self):
        return f"{self.customer.username}'s cart ({self.status})"

    class Meta:
        get_latest_by = 'date'

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cart_items')
    product = models.ForeignKey(Product, default='untitled_product', on_delete=models.SET_DEFAULT)
    quantity = models.PositiveIntegerField(default=1)
    chosen_attributes = models.ManyToManyField(Additional_choice_values, blank=True)

    def __str__(self):
        return f"user '{self.cart.customer.username}' ordered '{self.product.name}'"

    class Meta:
        get_latest_by = 'id'
