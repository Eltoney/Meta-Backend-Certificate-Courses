from rest_framework import serializers
from .models import Product, Category
from decimal import Decimal


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['title', 'slug']


class ProductSerialzier(serializers.ModelSerializer):
    stock = serializers.IntegerField(source='inventory')
    price_with_tax = serializers.SerializerMethodField(method_name='tax')
    # category = serializers.StringRelatedField()
    category = CategorySerializer()

    class Meta:
        model = Product
        fields = ['id', 'title', 'price',
                  'stock', 'category', 'price_with_tax']

    def tax(self, product: Product):
        return product.price * Decimal(1.14)
