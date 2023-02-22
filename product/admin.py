from django.contrib import admin
# from mptt.admin import MPTTModelAdmin
from django_mptt_admin.admin import DjangoMpttAdmin

from .models import *


class ProviderAdmin(admin.ModelAdmin):
    list_display = ('name', 'website_url', 'rating')

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'provider', 'price', 'available')

    def available(self, obj):
        return obj.stock.units > 0
        
    available.boolean = True

class CategoryAdmin(DjangoMpttAdmin):
    list_display = ('name', 'parent')
  

admin.site.register(Provider, ProviderAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Guarantee)
admin.site.register(Product_specs)
admin.site.register(Additional_choice_attributes)
admin.site.register(Additional_choice_values)
admin.site.register(Stock)
admin.site.register(Discount)