from rest_framework import serializers
from .models import Category
from .models import MenuItem
from decimal import Decimal


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'title', 'slug']


class MenuItemSerializer(serializers.ModelSerializer):
    stock = serializers.IntegerField(source='inventory')
    price_after_tax = serializers.SerializerMethodField(method_name='tax')
    category_id = serializers.IntegerField(write_only=True)
    category = CategorySerializer(read_only=True)

    class Meta:
        model = MenuItem
        fields = ['id', 'title', 'category_id', 'category',
                  'price', 'price_after_tax', 'stock']
        # depth = 1

    def tax(self, item: MenuItem):
        return item.price * Decimal(1.14)
