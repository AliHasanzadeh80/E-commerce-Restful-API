from django.urls import path

from .views import (
    CartList,
    UserCartList,
    UserCartDetail,
    UserCartItemDetail,
    OrderProduct,
)

urlpatterns = [
    path('product/<int:pk>/order/', OrderProduct.as_view(), name='order-product'),
    path('carts/', CartList.as_view(), name='cart-list'),
    path('account/my-carts/', UserCartList.as_view(), name='user-cart-list'),
    path('account/my-carts/<int:pk>/', UserCartDetail.as_view(), name='user-cart-detail'),
    path('account/my-carts/items/<int:pk>/', UserCartItemDetail.as_view(), name='user-cart-item-detail'),
]