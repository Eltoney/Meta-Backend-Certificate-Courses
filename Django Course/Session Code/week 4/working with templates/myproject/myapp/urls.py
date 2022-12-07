from django.urls import path
from . import views

urlpatterns = [
    path('welcome/<name>', views.index),
    path('', views.index),
    path('skills', views.skills),
    path('base', views.base),
    path('home/', views.home),
    path('login/', views.login),
    path('register/', views.register),
]
