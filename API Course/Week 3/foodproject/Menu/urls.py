from django.urls import path
from . import views
urlpatterns = [
    path('items', views.menu_items),
    path('items/<int:id>', views.single_item),
    path('menu-items', views.MenuItemsViewSet.as_view({'get': 'list'})),
    path('menu-items/<int:pk>',
         views.MenuItemsViewSet.as_view({'get': 'retrieve'})),
]
