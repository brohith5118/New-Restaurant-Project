from django.contrib import admin
from .models import User,Category,FoodItem,Order,OrderItem
# Register your models here.

admin.site.register(User)
admin.site.register(Category)
admin.site.register(FoodItem)
admin.site.register(Order)
admin.site.register(OrderItem)