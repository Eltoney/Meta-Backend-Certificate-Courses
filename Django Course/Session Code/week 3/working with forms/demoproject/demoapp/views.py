from django.shortcuts import render
from .forms import DrinkAdd
from django.http import HttpResponse

# Create your views here.


def from_view(request):
    form = DrinkAdd()
    if request.method == 'POST':
        form = DrinkAdd(request.POST)
        if form.is_valid():
            form.save()
    context = {'form': form}
    return render(request, 'myform.html', context)


def show_data(request, f):
    if request.method == 'POST':
        return HttpResponse(f'Hi {f.name} your age is {f.age}')
