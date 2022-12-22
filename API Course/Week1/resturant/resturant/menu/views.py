from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import Food
from django.forms.models import model_to_dict
from django.views.decorators.csrf import csrf_exempt


# Create your views here.

@csrf_exempt
def menu(request):
    if request.method == 'GET':
        data = []
        pk = request.GET.get('id')
        if pk is not None:
            try:
                data = Food.objects.get(pk=pk)
                data = model_to_dict(data)
            except Food.DoesNotExist:
                data = []
        else:
            data = list(Food.objects.all().values())
        return JsonResponse({'food': data})
    elif request.method == 'POST':
        name = request.POST.get('name')
        category = request.POST.get('category')
        price = request.POST.get('price')
        food = Food(name=name, category=category, price=price)
        try:
            food.save()
        except:
            return JsonResponse({'error': 'true', 'message': 'required field missing'}, status=400)
        return JsonResponse(model_to_dict(food), status=201)
