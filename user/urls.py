from django.urls import path

from .views import (
    registration,
    UserProfile,
    AddToFavorites, 
    RemoveFromFavorites
)


urlpatterns = [
    path('account/register/', registration, name='account-register'),

    path('account/profile/', UserProfile.as_view(), name='user-profile'),

    path('product/<int:product_pk>/add-to-favorites/', AddToFavorites.as_view(), name='add-to-favorites'),
    path('product/<int:product_pk>/remove-from-favorites/', RemoveFromFavorites.as_view(), name='remove-from-favorites'),
]