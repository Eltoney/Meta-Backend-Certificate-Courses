from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound, Http404
import datetime
# Create your views here.


def index(request):
    path = request.path
    method = request.method
    content = f''' 
        <center><h2>Testing Django Request Response Objects</h2> 
        <p>Request path : " {path}</p> 
        <p>Request Method :{method}</p></center> 
        '''
    return HttpResponse(content)


def user_page(request, name, id):
    return HttpResponse(f"Name: {name} UserId: {id + 5}")


def user_query(request):
    name = request.GET['name']
    id = request.GET['id']
    return HttpResponse(f"Name: {name} UserId: {id}")


def showform(request):
    return render(request, "form.html")


def getform(request):
    if request.method == "POST":
        id = request.POST['id']
        name = request.POST['name']
        return HttpResponse("Name:{} UserID:{}".format(name, id))
    else:
        return HttpResponse("Form not submitted <br> Go here: <a href='demoapp/showform'>Form </a>")


def current_datetime(request):
    now = datetime.datetime.now()
    html = f"<html><body> It is now: {now}.</body></html>"
    raise Http404(html)


def price(request, id):
    id = int(id)
    return HttpResponse(f'The price is {id + 100}')


def oops(request):
    condition = True
    if condition == True:
        raise Http404("Product not here bro")
    else:
        return HttpResponse('<h1>Page was found</h1>')


def year_count(request, year):
    return HttpResponse(year * 100)


def test(request, tr):
    return HttpResponse(tr + tr)
