from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage
from django.contrib.auth.models import User, Group
from .models import MenuItem, Cart, Category, Order, OrderItem
from .serializers import (MenuItemSerializer, UserSerializer, CartSerializer,
                          CategorySerializer, OrderSerializer, OrderItemSerializer)
from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes, throttle_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle
from django.db.models import Sum
from datetime import date
from decimal import Decimal
# Create your views here.


def cleanNullTerms(d):
    return {
        k: v
        for k, v in d.items()
        if v is not None
    }


@api_view(['GET', 'POST'])
@throttle_classes([UserRateThrottle])
@throttle_classes([AnonRateThrottle])
def all_menu_items(request):
    if request.method == 'GET':
        items = MenuItem.objects.select_related('category').all()
        category_name = request.query_params.get('category')
        to_price = request.query_params.get('to_price')
        search = request.query_params.get('search')
        ordering = request.query_params.get('ordering')
        perpage = request.query_params.get('perpage', default=10)
        page = request.query_params.get('page', default=1)
        if category_name:
            items = items.filter(category__title=category_name)
        if to_price:
            items = items.filter(price__lte=to_price)
        if search:
            items = items.filter(title__contains=search)
        if ordering:
            ordering_fields = ordering.split(",")
            items = items.order_by(*ordering_fields)
        paginator = Paginator(items, per_page=perpage)
        try:
            items = paginator.page(number=page)
        except EmptyPage:
            items = []
        serialized_item = MenuItemSerializer(items, many=True)
        return Response(serialized_item.data)
    elif request.method == 'POST':
        user = request.user
        if user.groups.filter(name='Manager').exists():
            serialized_item = MenuItemSerializer(data=request.data)
            serialized_item.is_valid(raise_exception=True)
            serialized_item.save()
            return Response(serialized_item.data, status=status.HTTP_201_CREATED)
        else:
            return Response({'message': 'You are Unauthorized to perform this operation'},
                            status=status.HTTP_403_FORBIDDEN)


@api_view(['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
def single_menu_item(request, item_id):
    if request.method == 'GET':
        item = get_object_or_404(MenuItem, pk=item_id)
        serialized_item = MenuItemSerializer(item)
        return Response(serialized_item.data)
    else:
        user = request.user
        if user.groups.filter(name='Manager').exists():
            if request.method == 'DELETE':
                item = get_object_or_404(MenuItem, pk=item_id)
                item.delete()
            elif request.method == 'POST':
                serialized_item = MenuItemSerializer(data=request.data)
                serialized_item.is_valid(raise_exception=True)
                serialized_item.save()
                return Response(serialized_item.data, status=status.HTTP_201_CREATED)
            elif request.method == 'PUT' or request.method == 'PATCH':
                attrs = {'title': None, 'price': None,
                         'category_id': None, 'featured': None}
                attrs['title'] = request.data.get('title')
                attrs['price'] = request.data.get('price')
                attrs['category_id'] = request.data.get('category_id')
                attrs['featured'] = request.data.get('featured')
                if attrs['featured'] == 'true':
                    attrs['featured'] = True
                elif attrs['featured'] == 'false':
                    attrs['featured'] = False
                attrs = cleanNullTerms(attrs)

                MenuItem.objects.filter(pk=item_id).update(**attrs)
                serialized_item = MenuItemSerializer(
                    MenuItem.objects.get(pk=item_id))
                return Response(serialized_item.data)
        else:
            return Response({'message': 'You are Unauthorized to perform this operation'},
                            status=status.HTTP_403_FORBIDDEN)


@api_view(['GET', 'POST'])
def manager_users(request):
    user = request.user
    if user.is_superuser:
        if request.method == 'GET':
            items = User.objects.filter(groups__name='Manager').all()
            serialized_item = UserSerializer(items, many=True)
            return Response(serialized_item.data)
        else:
            username = request.data['username']
            if username:
                user = get_object_or_404(User,  username=username)
                managers = Group.objects.get(name="Manager")
                managers.user_set.add(user)
                return Response({'message': 'ok'}, status=status.HTTP_201_CREATED)
            return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    elif user.groups.filter(name='Manager').exists():
        if request.method == 'GET':
            items = User.objects.filter(groups__name='Manager').all()
            serialized_item = UserSerializer(items, many=True)
            return Response(serialized_item.data)
        else:
            username = request.data['username']
            if username:
                user = get_object_or_404(User,  username=username)
                managers = Group.objects.get(name="Delivery Crew")
                managers.user_set.add(user)
                return Response({'message': 'ok'}, status=status.HTTP_201_CREATED)
            return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    else:
        return Response({'message': 'You are Unauthorized to perform this operation'},
                        status=status.HTTP_403_FORBIDDEN)


@api_view(['DELETE'])
def manager_user(request, username):
    user = request.user
    if user.groups.filter(name='Manager').exists():
        user = get_object_or_404(User, username=username)
        managers = Group.objects.get(name="Manager")
        managers.user_set.remove(user)
        return Response({'message': 'ok'})
    else:
        return Response({'message': 'You are Unauthorized to perform this operation'},
                        status=status.HTTP_403_FORBIDDEN)


@api_view(['GET', 'POST'])
def delivery_users(request):
    user = request.user
    if user.groups.filter(name='Manager').exists():
        if request.method == 'GET':
            items = User.objects.filter(groups__name='Delivery Crew').all()
            serialized_item = UserSerializer(items, many=True)
            return Response(serialized_item.data)
        else:
            username = request.data['username']
            if username:
                user = get_object_or_404(User,  username=username)
                managers = Group.objects.get(name="Delivery Crew")
                managers.user_set.add(user)
                return Response({'message': 'ok'}, status=status.HTTP_201_CREATED)
            return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    else:
        return Response({'message': 'You are Unauthorized to perform this operation'},
                        status=status.HTTP_403_FORBIDDEN)


@api_view(['DELETE'])
def delivery_user(request, username):
    user = request.user
    if user.groups.filter(name='Manager').exists():
        user = get_object_or_404(User, username=username)
        managers = Group.objects.get(name="Delivery Crew")
        managers.user_set.remove(user)
        return Response({'message': 'ok'})
    else:
        return Response({'message': 'You are Unauthorized to perform this operation'},
                        status=status.HTTP_403_FORBIDDEN)


@api_view(['GET', 'POST', 'DELETE'])
@permission_classes([IsAuthenticated])
def cart(request):
    user_id = request.user.id
    if request.method == 'GET':
        items = Cart.objects.filter(user_id=user_id).all()
        serialized_items = CartSerializer(items, many=True)
        return Response(serialized_items.data)
    elif request.method == 'DELETE':
        items = Cart.objects.filter(user_id=user_id).all().delete()
        return Response({'message': 'ok'})
    else:
        item_title = request.data['menuitem'].lower()
        item_quantity = int(request.data.get('quantity'))
        unit_price = int(request.data.get('unit_price'))
        item = get_object_or_404(MenuItem, title=item_title)
        if unit_price is None:
            unit_price = item.price
        cart_item = Cart(user=User.objects.get(pk=user_id), menuitem=item, unit_price=unit_price,
                         quantity=item_quantity, price=unit_price * item_quantity)
        try:
            cart_item.save()
        except:
            return Response({'message': 'transaction has failed'}, status=status.HTTP_406_NOT_ACCEPTABLE)
        return Response({'message': f'{item_quantity} of {item_title} has been added succesfully'},
                        status=status.HTTP_201_CREATED)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def all_orders(request):
    user = request.user
    if request.method == 'POST':
        cart = Cart.objects.filter(user_id=user.id).all()
        total = cart.aggregate(Sum('price'))['price__sum']
        cur_date = date.today()
        user_id = user.id
        order = Order(total=total, user_id=user_id,
                      date=cur_date, status=0, delivery_crew=None)
        order.save()

        for item in cart:
            order_item = OrderItem(order_id=order.id, menuitem_id=item.menuitem_id, quantity=item.quantity,
                                   unit_price=item.unit_price, price=item.price)
            order_item.save()

        Cart.objects.filter(user_id=user.id).all().delete()
        return Response({'message': 'ok'}, status=status.HTTP_201_CREATED)
    else:
        if user.groups.filter(name='Manager').exists():
            items = Order.objects.all()
            serialized_item = OrderSerializer(items, many=True)
            return Response(serialized_item.data)
        elif user.groups.filter(name='Delivery Crew').exists():
            items = Order.objects.filter(delivery_crew_id=user.id).all()
            serialized_item = OrderSerializer(items, many=True)
            return Response(serialized_item.data)
        else:
            items = Order.objects.filter(user_id=user.id).all()
            serialized_item = OrderSerializer(items, many=True)
            return Response(serialized_item.data)


@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
@permission_classes([IsAuthenticated])
def single_order(request, order_id):
    user = request.user
    if request.method == 'GET':
        order = get_object_or_404(Order, pk=order_id)
        if order.user_id == user.id:
            items = OrderItem.objects.filter(order_id=order_id).all()
            serialized_items = OrderItemSerializer(items, many=True)
            return Response(serialized_items.data)
        return Response({'message': 'Not authorized'}, status=status.HTTP_401_UNAUTHORIZED)
    elif request.method == 'DELETE':
        if user.groups.filter(name='Manager').exists():
            OrderItem.filter(order_id=order_id).all().delete()
            Order.filter(pk=order_id).all().delete()
            return Response({'message': 'success'})
        return Response({'message': 'Not authorized'}, status=status.HTTP_401_UNAUTHORIZED)
    else:
        if user.groups.filter(name='Manager').exists():
            attrs = {'status': None, 'delivery_crew_id': None}
            attrs['status'] = request.data.get('status')
            attrs['delivery_crew_id'] = request.data.get('delivery_crew')
            attrs = cleanNullTerms(attrs)

            Order.objects.filter(pk=order_id).update(**attrs)
            return Response({'message': 'success'})
        elif user.groups.filter(name='Delivery Crew').exists():
            order = Order.objects.get(pk=order_id)
            if order.delivery_crew.id == user.id:
                ship = request.data.get('status')
                if ship:
                    if ship == 'true':
                        ship = True
                    else:
                        ship = False
                    Order.objects.filter(pk=order_id).update(status=ship)
                    return Response({'message': 'success'})
                return Response({'message': 'failed status'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'message': 'Not authorized'}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['GET', 'POST'])
def categories_list(request):
    if request.method == 'GET':
        items = Category.objects.all()
        serialized_items = CategorySerializer(items, many=True)
        return Response(serialized_items.data)
    else:
        user = request.user
        if user.groups.filter(name='Manager').exists():
            serialized_item = CategorySerializer(data=request.data)
            serialized_item.is_valid(raise_exception=True)
            serialized_item.save()
            return Response(serialized_item.data, status=status.HTTP_201_CREATED)
        return Response({'message': 'unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['GET', 'POST'])
def featured_list(request):
    if request.method == 'GET':
        items = MenuItem.objects.filter(featured=1).all()
        serialized_items = MenuItemSerializer(items, many=True)
        return Response(serialized_items.data)
    else:
        user = request.user
        if user.groups.filter(name='Manager').exists():
            title = request.data['item']
            item = get_object_or_404(MenuItem, title=title)
            val = 1
            if item.featured == 1:
                val = 0
            MenuItem.objects.filter(title=title).update(featured=val)
            return Response({'message': 'ok'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'message': 'Not Authorized'}, status=status.HTTP_401_UNAUTHORIZED)
