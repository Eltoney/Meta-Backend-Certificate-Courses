from django.urls import path
from . import views

urlpatterns = [
    path('item/<int:id>', views.item_show, name="item-show"),
]
