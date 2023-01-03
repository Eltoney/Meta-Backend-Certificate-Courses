from . import views
from django.urls import path

urlpatterns = [
    path('blog/', views.form_view, name="blog"),
]
