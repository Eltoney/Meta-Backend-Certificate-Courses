from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import MenuItem, Category
from .serializers import MenuItemSerializer, CategorySerializer
from django.shortcuts import get_object_or_404
from rest_framework import status

# Create your views here.


@api_view(['GET', 'POST'])
def menu_items(request):
    if request.method == 'GET':
        items = MenuItem.objects.select_related('category').all()
        serialized_item = MenuItemSerializer(items, many=True)
        return Response(serialized_item.data)
    elif request.method == 'POST':
        serialized_item = MenuItemSerializer(data=request.data)
        serialized_item.is_valid(raise_exception=True)
        serialized_item.save()
        return Response(serialized_item.data, status=status.HTTP_201_CREATED)


@api_view(['GET', 'PUT', 'DELETE'])
def single_item(request, id):
    if request.method == 'GET':
        item = get_object_or_404(MenuItem, pk=id)
        serialized_item = MenuItemSerializer(item)
        return Response(serialized_item.data)
    elif request.method == 'PUT':
        newAttrs = {}
        title = request.data.get('title')
        if title:
            newAttrs['title'] = title
        price = request.data.get('price')
        if price:
            newAttrs['price'] = price
        inventory = request.data.get('title')
        if inventory:
            newAttrs['inventory'] = inventory
        category = request.data.get('category')
        if category:
            newAttrs['category'] = category
        MenuItem.objects.filter(pk=id).update(**newAttrs)
        item = get_object_or_404(MenuItem, pk=id)
        serialized_item = MenuItemSerializer(item)
        return Response(serialized_item.data)
    elif request.method == 'DELETE':
        item = get_object_or_404(MenuItem, pk=id)
        item.delete()
        return Response('Delete Succesfully')
