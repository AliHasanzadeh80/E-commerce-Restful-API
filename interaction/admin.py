from django.contrib import admin

from mptt.admin import MPTTModelAdmin
from django_mptt_admin.admin import DjangoMpttAdmin

from .models import Comment, Rating

class CommentAdmin(DjangoMpttAdmin):
    list_display = ('user', 'parent', 'product', 'content')

class RatingAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'value')

admin.site.register(Comment, CommentAdmin)
admin.site.register(Rating, RatingAdmin)
