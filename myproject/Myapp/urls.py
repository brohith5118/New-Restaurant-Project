from django.urls import path
from . import views

urlpatterns = [
    path('',views.home),

    #login
    path('login_view',views.login_view),
    path('logout_view',views.logout_view),

    #customer
    path('menu',views.menu),
    path('menu/item_details',views.item_details),
    path('user_order',views.user_order),
    path('user_order_history',views.user_order_history),

    #manager
    path('manager',views.manager),
    path('current_orders',views.current_orders),
    path('categories',views.categories),
    path('food_items',views.food_items),
    path('room_view',views.room_view),
    path('orders_history',views.orders_history)
]