from django.urls import path

from .views import (
    ProductList,
    ProductDetail,
    StockDetail,
    DiscountDetail,
    ProviderList,
    ProviderDetail,
    ProviderProducts,
    CategoryList,
    CategoryDetail,
    GuaranteeList,
    GuaranteeDetail
)


urlpatterns = [
    path('all/', ProductList.as_view(), name='product-list'),
    path('<int:pk>/', ProductDetail.as_view(), name='product-detail'),
    path('<int:product_pk>/stock/', StockDetail.as_view(), name='product-stock'),
    path('<int:product_pk>/remove-discount/', DiscountDetail.as_view(), name='remove-discount'),

    path('providers/', ProviderList.as_view(), name='provider-list'),
    path('providers/<int:pk>/', ProviderDetail.as_view(), name='provider-detail'),
    path('providers/<int:pk>/products/', ProviderProducts.as_view(), name='provider-products'),

    path('categories/', CategoryList.as_view(), name='category-list'),
    path('categories/<int:pk>/', CategoryDetail.as_view(), name='category-detail'),

    path('guarantees/', GuaranteeList.as_view(), name='guarantee-list'),
    path('guarantees/<int:pk>/', GuaranteeDetail.as_view(), name='guarantee-detail')
]