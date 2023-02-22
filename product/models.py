from django.db import models

from mptt.models import MPTTModel, TreeForeignKey


class Category(MPTTModel):
    name = models.CharField("category name", max_length=100, unique=True)
    parent = TreeForeignKey('self', on_delete=models.PROTECT, null=True, blank=True, related_name='sub_categories')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'categories'

class Provider(models.Model):
    name = models.CharField("provider name", max_length=100, unique=True)
    website_url = models.CharField(max_length=255, blank=True, null=True)
    rating = models.DecimalField(default=0, decimal_places=1, max_digits=2, null=True, blank=True)

    def __str__(self):
        return self.name
        
    class Meta:
        verbose_name = 'Product Provider'

class Guarantee(models.Model):
    name = models.CharField("guarantee name", max_length=100, blank=True, null=True)
    website_url = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    categories = models.ManyToManyField(Category)
    provider = models.ForeignKey(Provider, default='unknown', on_delete=models.SET_DEFAULT, related_name='product')
    name = models.CharField("product name", max_length=100)
    price = models.DecimalField(decimal_places=2, max_digits=10)
    average_rating = models.DecimalField(decimal_places=1, max_digits=2, null=True, blank=True)
    description = models.TextField(blank=True, null=True)
    guarantee = models.ForeignKey(Guarantee, on_delete=models.CASCADE, null=True, blank=True)
    
    def __str__(self):
        return self.name
    
    @property
    def final_price(self):
        try:
            return (self.price - (self.discount.amount * self.price)/100)
        except ValueError:
            return self.price

    @property
    def comments_count(self):
        return self.comments.count()

class Product_specs(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='specs')
    attribute = models.CharField(max_length=100)
    value = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.product.name}) {self.attribute}:{self.value}"
    
    class Meta:
        verbose_name_plural = 'product specs'
        verbose_name = 'Product Specification'

class Additional_choice_attributes(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='additional_choices')
    attribute = models.CharField(max_length=80)

    def __str__(self):
        return f"{self.product.name}) {self.attribute}"

    class Meta:
        verbose_name_plural = 'additional choice attributes'
        verbose_name = 'Additional Product Attribute'

class Additional_choice_values(models.Model):
    attribute = models.ForeignKey(Additional_choice_attributes, on_delete=models.CASCADE, related_name='attribute_value')
    value = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.attribute}:{self.value}"

    class Meta:
        verbose_name_plural = 'additional choice values'
        verbose_name = 'Additional Product Value'

class Stock(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name='stock')
    units = models.PositiveIntegerField()
    units_sold = models.PositiveIntegerField(default=0)
    last_sold = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.product.name}) available:{self.units}, sold:{self.units_sold}"

    class Meta:
        verbose_name_plural = 'stocks'
        verbose_name = 'Product Stock'
        get_latest_by = 'last_sold'
        
class Discount(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name='discount', null=True)
    amount = models.PositiveSmallIntegerField()
    time_left = models.TimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.amount}% discount on {self.product.name}"