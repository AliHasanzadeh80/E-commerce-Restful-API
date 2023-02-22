from django.db.models import Count

from rest_framework import generics
from rest_framework import filters
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAdminUser, IsAuthenticated

from .models import Cart, CartItem
from product.models import Product, Additional_choice_values
from .serializers import CartSerializer, CartItemSerializer


class CartList(generics.ListAPIView):
    serializer_class = CartSerializer
    queryset = Cart.objects.all()
    permission_classes = [IsAdminUser]

class UserCartList(generics.ListAPIView):
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['date']

    def get_queryset(self):
        return Cart.objects.filter(customer=self.request.user)

class UserCartDetail(generics.RetrieveDestroyAPIView):
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Cart.objects.filter(customer=self.request.user)

class UserCartItemDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CartItemSerializer
    queryset = CartItem.objects.all()
    
class OrderProduct(generics.CreateAPIView):
    serializer_class = CartItemSerializer
    queryset = CartItem.objects.all()
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user
        product = Product.objects.get(pk=self.kwargs['pk'])
        quantity = serializer.validated_data.get('quantity', 1)
        chosen_attributes = serializer.validated_data.get('chosen_attributes', Additional_choice_values.objects.none())
        cart, created = Cart.objects.get_or_create(customer=user, status='in-process')

        to_filter = CartItem.objects.filter(
            cart=cart,
            product=product,
        ).annotate(num_attr=Count('chosen_attributes')
        ).filter(num_attr=len(chosen_attributes))

        for attr in chosen_attributes:
            to_filter = to_filter.filter(chosen_attributes=attr)

        if product.stock.units >= quantity:
            if not created and to_filter.exists():
                raise ValidationError('This items is already in your cart.')
            else:
                serializer.save(cart=cart, product=product)
                product.stock.units_sold = product.stock.units_sold + quantity
                product.stock.units = product.stock.units - quantity
                product.stock.save()
        else:
            raise ValidationError('Unfortunately this product is currently unavailable.')
