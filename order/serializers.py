from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from drf_writable_nested import WritableNestedModelSerializer

from .models import Cart, CartItem
from product.models import Product


class CartItemSerializer(serializers.ModelSerializer):
    product = serializers.SlugRelatedField(
        queryset=Product.objects.all(),
        slug_field='name',
        required=False
    )
    chosen_attributes = serializers.SlugRelatedField(
        many=True,
        slug_field='value',
        read_only=True
    )

    class Meta:
        model = CartItem
        exclude = ('cart',)

    def update(self, instance, validated_data):
        new_quantity = validated_data['quantity']
        product = validated_data['product']
        prev_quantity = instance.quantity
        quantity_diff = abs(new_quantity-prev_quantity)

        if new_quantity > prev_quantity:
            if new_quantity > product.stock.units:
                raise ValidationError('Unfortunately this product is currently unavailable.')

            product.stock.units = product.stock.units - quantity_diff
            product.stock.units_sold = product.stock.units_sold + quantity_diff

        elif prev_quantity > new_quantity:
            product.stock.units = product.stock.units + quantity_diff
            product.stock.units_sold = product.stock.units_sold - quantity_diff
            
        product.stock.save()

        if new_quantity != 0:
            instance.quantity = new_quantity
            instance.save()
        else:
            instance.delete()

        return instance

class CartSerializer(
    WritableNestedModelSerializer, 
    serializers.ModelSerializer
):
    customer = serializers.CharField(max_length=50, read_only=True)
    cart_items = CartItemSerializer(many=True)

    class Meta:
        model = Cart
        fields = '__all__'
