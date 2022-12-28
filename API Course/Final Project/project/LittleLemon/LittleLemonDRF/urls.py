from django.urls import path
from . import views
urlpatterns = [
    path('menu-items', views.all_menu_items),
    path('menu-items/<int:item_id>', views.single_menu_item),
    path('groups/manager/users', views.manager_users),
    path('groups/manager/users/<str:username>', views.manager_user),
    path('groups/delivery-crew/users', views.delivery_users),
    path('groups/delivery-crew/users/<str:username>', views.delivery_user),
    path('cart/menu-items', views.cart),
    # path('cart/order',view)
    path('orders', views.all_orders),
    path('orders/<int:order_id>', views.single_order),
    path('featured', views.featured_list),
    path('categories', views.categories_list),
]
