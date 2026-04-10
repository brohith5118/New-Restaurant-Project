from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('',views.home,name='home'),

    #login
    path('login_view',views.login_view),
    path('logout_view',views.logout_view),

    #customer
    path('menu',views.menu),
    path('menu/item_details/<int:id>',views.item_details),
    path('user_order',views.user_order),
    path('user_order_history',views.user_order_history),
    path('add-to-cart/', views.add_to_cart, name='add_to_cart'),
    path('update-cart/', views.update_cart, name='update_cart'),
    path('get-cart/', views.get_cart, name='get_cart'),

    #manager
    path('manager',views.manager),
    path('current_orders',views.current_orders),
    path('categories',views.categories),
    path('food_items',views.food_items),
    path('room_view',views.room_view),
    path('orders_history',views.orders_history),
    path('add_food_item',views.add_food_item),
    path('edit_item/<int:id>',views.edit_item,name="editItem"),
    path('edit_item/edit_item/<int:id>',views.edit_item),
    path('delete_item/<int:id>',views.delete_item),
    path('about',views.about),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)