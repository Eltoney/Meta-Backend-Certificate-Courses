from django.shortcuts import render
from django.http import HttpResponse
from .models import Menu
from .models import MenuCategory
# Create your views here.


def item_show(request, id):
    try:
        obj = Menu.objects.get(pk=id)
        try:
            cus = MenuCategory.objects.get(pk=obj.category_id)
            return HttpResponse(f'Your item is {obj.menu_item} from \
            {cus.menu_category_name} with a price {obj.price}')
        except:
            return HttpResponse(f'The item {obj.menu_item} is with price {obj.price}')
    except:
        return HttpResponse('Opps , item not found')
