from django.http import HttpResponse


def homepage(request):
    return HttpResponse('Welcome at TLK resturant')
