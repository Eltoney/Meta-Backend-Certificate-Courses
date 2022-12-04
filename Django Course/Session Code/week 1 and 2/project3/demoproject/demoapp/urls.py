from django.urls import path, re_path, register_converter
from . import views, converters
app_name = 'demoapp'

register_converter(converters.FourDigitYearConvertor, 'yyyy')


urlpatterns = [
    path('', views.index, name='index'),
    path('getuser/<name>/<int:id>', views.user_page, name="user_page"),
    path('queryuser/', views.user_query, name="query_page"),
    path('showform/', views.showform, name="showform"),
    path('getform/', views.getform, name="getform"),
    path('curtime/', views.current_datetime, name="curTime"),
    path('price/<int:id>', views.price, name='price'),
    re_path(r'^price/([0-9]{2})/$', views.price, name='price'),
    path('oops', views.oops, name='oops'),
    path('mul/<yyyy:year>', views.year_count, name='years'),
    re_path(r'^test/(?P<tr>[0-9]{4})/$' , views.test),
    # re_path(r'^test/(P<tr>[1-9])/$', views.test)
    #re_path(r'^home/(?P<int:travel>[1-99])/$' , views.test , name = 'test')
]
