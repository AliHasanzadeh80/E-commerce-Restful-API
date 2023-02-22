from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from django.core.validators import MinValueValidator, MaxValueValidator

from django.contrib.auth.models import User
from product.models import Product


class Comment(MPTTModel):
    user = models.ForeignKey(User, default='anonymous', on_delete=models.SET_DEFAULT)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='sub_comments')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()

    def __str__(self):
        return self.content

class Rating(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='rating')
    value = models.PositiveSmallIntegerField('rating value', validators=[MinValueValidator(0), MaxValueValidator(5)])

    def __str__(self):
        return f"{self.product.name}:{self.value}"
