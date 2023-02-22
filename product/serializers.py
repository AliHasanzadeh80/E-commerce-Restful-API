from rest_framework import serializers

from drf_writable_nested import WritableNestedModelSerializer

from .models import *


class CategorySerializer(serializers.ModelSerializer):
    sub_categories = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='category-detail'
    )
    parent = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='name',
        required=False
    )
   
    class Meta:
        model = Category
        fields = ('id', 'name', 'parent', 'sub_categories')

class ProductSpecsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product_specs
        exclude = ('id', 'product')

class AdditionalValuesSerialize(
    WritableNestedModelSerializer, 
    serializers.Serializer
):
    value = serializers.CharField(max_length=50)
    
    class Meta:
        model = Additional_choice_values
        fields = ('value',)

class AdditionalAttributesSerializer(
    WritableNestedModelSerializer, 
    serializers.ModelSerializer
):
    attribute_value = AdditionalValuesSerialize(many=True)

    class Meta:
        model = Additional_choice_attributes
        exclude = ('id', 'product')

class DiscountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Discount
        fields = ('amount', 'time_left')

class GuaranteeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Guarantee
        fields  ='__all__'

class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = ('units', 'units_sold', 'last_sold')

class ProductSerializer(
        WritableNestedModelSerializer, 
        serializers.ModelSerializer
    ):
    categories = serializers.SlugRelatedField(
        many=True,
        queryset=Category.objects.all(),
        slug_field='name',
    )
    provider = serializers.SlugRelatedField(
        queryset=Provider.objects.all(),
        slug_field='name',
    )
    guarantee = serializers.SlugRelatedField(
        queryset=Guarantee.objects.all(),
        slug_field='name',
    )

    discount = DiscountSerializer(required=False)
    specs = ProductSpecsSerializer(many=True)
    additional_choices = AdditionalAttributesSerializer(many=True)
    stock = StockSerializer(required=True)
   
    class Meta:
        model = Product
        fields = '__all__'

    def create(self, validated_data):
        specs = validated_data.pop('specs')
        additional_choices = validated_data.pop('additional_choices')
        categories = validated_data.pop('categories')
        stock = dict(validated_data.pop('stock'))

        instance = Product.objects.create(**validated_data)
        instance.categories.add(*categories)

        Stock.objects.create(product=instance, units=stock['units'])
             
        for spec in specs:
            spec_dict = dict(spec)
            Product_specs.objects.create(product=instance, attribute=spec_dict['attribute'], value=spec_dict['value'])
        
        for add_choice in additional_choices:
            add_choice_dict = dict(add_choice)
            attribute = add_choice_dict['attribute']
            values = add_choice_dict['attribute_value']
            attrib_instance = Additional_choice_attributes.objects.create(product=instance, attribute=attribute)
            for value in values:
                pure_value = dict(value)['value']
                Additional_choice_values.objects.get_or_create(attribute=attrib_instance, value=pure_value)

        return instance

class ProviderSerializer(serializers.ModelSerializer):
    product = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='product-detail'
    )

    class Meta:
        model = Provider
        fields = '__all__'
