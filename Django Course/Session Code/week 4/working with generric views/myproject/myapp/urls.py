from django.urls import path
from . import views

urlpatterns = [
    # path('new/' , views.NewView.as_view()),
    # path('' , views.HomeView.as_view()),
    path('success/', views.sucess),
    path('create/', views.EmployeeCreate.as_view(), name='EmployeeCreate'),
    path('list/', views.EmployeeList.as_view()),
    path('show/<int:pk>', views.EmployeeDetail.as_view()),
    path('update/<int:pk>', views.EmployeeUpdate.as_view(), name = 'EmployeeUpdate'),
    path('delete/<int:pk>', views.EmployeeDelete.as_view(), name = 'EmployeeDelete') 
]
