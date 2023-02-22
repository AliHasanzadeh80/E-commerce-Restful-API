from django.db.models import ProtectedError
from django.http import Http404

from .models import *

from .serializers import (
    CategorySerializer,
    ProductSerializer,
    ProviderSerializer,
    GuaranteeSerializer,
    DiscountSerializer,
    StockSerializer
)

from rest_framework import generics
from rest_framework import filters
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAdminUser

from django_filters.rest_framework import DjangoFilterBackend

from .permissions import IsAdminOrReadOnly
from .pagination import ProductPagination


class ProductList(generics.ListCreateAPIView):
    serializer_class = ProductSerializer
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = ProductPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['name', 'provider__name', 'guarantee__name']
    search_fields = ['name', 'description']
    ordering_fields = ['id', 'price', 'average_rating']

    def get_queryset(self):
        queryset = Product.objects.all()
        filter_categories = self.request.query_params.get('categories')
        min_price = self.request.query_params.get('min-price')
        max_price = self.request.query_params.get('max-price')
        min_ratingAVG = self.request.query_params.get('min-rating')

        if filter_categories:
            queryset = queryset.filter(categories__name__in=filter_categories.split(','))
        if min_price and max_price:
            queryset = queryset.filter(price__lte=max_price, price__gte=min_price)
        if min_ratingAVG:
            queryset = queryset.filter(average_rating__gte=min_ratingAVG)

        return queryset
   
class ProductDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAdminOrReadOnly]

class CategoryList(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]

class CategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminUser]

    def perform_destroy(self, instance):
        try:
            return instance.delete()
        except ProtectedError as e:
            raise ValidationError(e)

class ProviderList(generics.ListCreateAPIView):
    queryset = Provider.objects.all()
    serializer_class = ProviderSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['rating']

class ProviderDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Provider.objects.all()
    serializer_class = ProviderSerializer
    permission_classes = [IsAdminOrReadOnly]

class ProviderProducts(generics.ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        pk = self.kwargs.get('pk')
        return Product.objects.filter(provider__id=pk)

class GuaranteeList(generics.ListCreateAPIView):
    queryset = Guarantee.objects.all()
    serializer_class = GuaranteeSerializer
    permission_classes = [IsAdminOrReadOnly]

class GuaranteeDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = GuaranteeSerializer
    queryset = Guarantee.objects.all()
    permission_classes = [IsAdminOrReadOnly]

class DiscountDetail(generics.DestroyAPIView):
    serializer_class = DiscountSerializer
    queryset = Discount.objects.all()
    permission_classes = [IsAdminUser]

    def get_object(self):
        try:
            return Discount.objects.get(product__id=self.kwargs['product_pk'])
        except Discount.DoesNotExist:
            raise Http404

class StockDetail(generics.RetrieveAPIView):
    serializer_class = StockSerializer
    queryset = Stock.objects.all()

    def get_object(self):
        try:
            return Stock.objects.get(product__id=self.kwargs['product_pk'])
        except Stock.DoesNotExist:
            raise Http404
