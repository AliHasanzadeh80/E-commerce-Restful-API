from django.urls import path

from .views import (
    ProductCommentsList,
    ProductCommentDetail,
    AddProductComment,
    UserCommentsList,
    RateProduct,
)

urlpatterns = [
    path('product/<int:product_pk>/comments/', ProductCommentsList.as_view(), name='product-comments'),
    path('product/comments/<int:pk>/', ProductCommentDetail.as_view(), name='product-comment-detail'),

    path('product/<int:product_pk>/add-comment/', AddProductComment.as_view(), name='product-comments'),

    path('product/<int:product_pk>/rate/', RateProduct.as_view(), name='rate-product'),

    path('account/comments/', UserCommentsList.as_view(), name='user-comments-list'),
]