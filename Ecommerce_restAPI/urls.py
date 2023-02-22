from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('product/', include('product.urls')),
    path('', include('order.urls')),
    path('', include('interaction.urls')),
    path('', include('user.urls')),
    path('api-auth/', include('rest_framework.urls')),
]
