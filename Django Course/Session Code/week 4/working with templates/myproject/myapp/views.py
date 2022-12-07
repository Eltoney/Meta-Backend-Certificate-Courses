from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

# Create your views here.


def home(request):
    return render(request, 'home.html', {})


def register(request):
    return render(request, 'register.html', {})


def login(request):
    return render(request, 'login.html', {})


def index(request, name='Ali'):
    template = loader.get_template('index.html')
    name = name.capitalize()
    expression = name.startswith('A')
    context = {"name": name, "expression": expression}
    return HttpResponse(template.render(context, request))


def skills(request):
    # skills = {{"python": 70}, {"django": 20}}
    # context = {"skills" : skills}
    # template = loader.get_template('myskills.html')
    # return HttpResponse(template.render(context, request))
    context = {"data": [
        {"name": "python", "prof": 70},
        {"name": "django", "prof": 20},
    ]}
    return render(request, 'myskills.html', context)


def base(request):
    return render(request, 'base.html')
