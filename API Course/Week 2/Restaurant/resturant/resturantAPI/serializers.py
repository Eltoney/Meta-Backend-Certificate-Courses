from rest_framework import serializers
from .models import MenuItem
from decimal import Decimal

class MenuItemSerializer(serializers.ModelSerializer):
    price_after_tax = serializers.SerializerMethodField(method_name='tax')
    stock = serializers.IntegerField(source='inventory')

    class Meta:
        model = MenuItem
        fields = ['id', 'title', 'price', 'price_after_tax', 'stock']

    def tax(self, product: MenuItem):
        return product.price * Decimal(0.14)
