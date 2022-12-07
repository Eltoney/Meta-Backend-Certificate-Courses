from django.shortcuts import render
from django.views import View
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView
from django.views.generic.edit import DeleteView 
from django.http import HttpResponse
from .models import Employee
# Create your views here.

class NewView(View):
    def get(self , request):
        return HttpResponse('Response Wow')

class HomeView(TemplateView):
    template_name: str = 'home.html'

def sucess(request):
    return HttpResponse('<h1>Sucess Operation</h1>')

class EmployeeCreate(CreateView):
    model = Employee
    fields = '__all__'
    success_url = "/employee/success"

class EmployeeList(ListView):
    model = Employee
    success_url = "/employee/success"

class EmployeeDetail(DetailView):
    model = Employee
    success_url = "/employee/success"

class EmployeeUpdate(UpdateView):   
    model = Employee   
    fields = '__all__'   
    success_url = "/employee/success/"

class EmployeeDelete(DeleteView):   
    model = Employee   
    success_url = "/employee/success/"  



