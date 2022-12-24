from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404
from .models import Product, Category
from .serializers import ProductSerialzier


@api_view()
def test(request):
    return Response('Hi')

@api_view()
def all_products(request):
    items = Product.objects.select_related('category').all()
    serialized_item = ProductSerialzier(items, many=True)
    return Response(serialized_item.data)

@api_view()
def single_product(request, id):
    item = get_object_or_404(Product, pk=id)
    serialized_item = ProductSerialzier(item)
    return Response(serialized_item.data)
