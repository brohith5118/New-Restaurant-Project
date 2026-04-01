from django.db import models
from django.utils import timezone

# 👤 USER MODEL (Room + Manager)
class User(models.Model):
    ROLE_CHOICES = [
        ('room', 'Room'),
        ('manager', 'Manager'),
    ]

    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=50)
    room_number = models.IntegerField(null=True, blank=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='room')

    def __str__(self):
        return f"{self.username} ({self.role})"


# 🍱 CATEGORY
class Category(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='category_images/', null=True, blank=True)

    def __str__(self):
        return self.name


# 🍔 FOOD ITEM
class FoodItem(models.Model):
    name = models.CharField(max_length=100)
    price = models.FloatField()
    description = models.TextField(blank=True)

    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    image = models.ImageField(upload_to='food_images/', null=True, blank=True)

    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


# 📦 ORDER
class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('preparing', 'Preparing'),
        ('out_for_delivery', 'Out for Delivery'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    total_price = models.FloatField(default=0)

    # important for history
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Order {self.id} - {self.user.username} - {self.status}"


# 🧾 ORDER ITEMS
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')

    food_item = models.ForeignKey(FoodItem, on_delete=models.CASCADE)

    quantity = models.IntegerField(default=1)

    price = models.FloatField(default=0)  # store price at time of order

    def __str__(self):
        return f"{self.food_item.name} x {self.quantity}"