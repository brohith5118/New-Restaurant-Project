from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.http import JsonResponse
from .models import User,Category,Order,OrderItem,FoodItem,Cart, CartItem


# Create your views here.
#login Page
def home(request):
    user_id = request.session.get('user_id')
    username = request.session.get('username')
    role = request.session.get('role')

    return render(request,'home.html',{
        'user_id':user_id,
        'username':username,
        'role':role
    })

def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username, password=password)

            # store session
            request.session['username'] = username
            request.session['user_id'] = user.id
            request.session['role'] = user.role

            return redirect('home')

        except User.DoesNotExist:
            return HttpResponse("Invalid credentials")

    return render(request, 'login_view.html')


def logout_view(request):
    request.session.flush()
    return redirect('/')

def is_logged_in(request):
    return request.session.get('user_id')

def about(request):
    return render(request,'about.html')


#Customers Views
def menu(request):
    if not is_logged_in(request):
        return redirect('/login_view')
    
    categories = Category.objects.all()
    food_items = FoodItem.objects.all()

    userName = request.session.get('username')
    return render(request,'menu.html',{
        'userName':userName,
        'categories':categories,
        'foodItems':food_items
        })


def item_details(request,id):
    if not is_logged_in(request):
        return redirect('/login_view')
    
    food_item = FoodItem.objects.get(id=id)
    itemcart = CartItem.objects.filter(cart__user_id=request.session.get('user_id'), food_item_id=id).first()
    cart = CartItem.objects.filter(cart__user_id=request.session.get('user_id'))

    return render(request,'item_details.html',{
        'foodItem':food_item,
        'cart': cart,
        'itemcart': itemcart,
    })


def cart_view(request):
    if not is_logged_in(request):
        return redirect('/login_view')
    
    cart_items = CartItem.objects.filter(cart__user_id=request.session.get('user_id')).select_related('food_item')
    for item in cart_items:
        item.total_price = item.quantity * item.food_item.price
    
    return render(request,'cart_view.html',{
        'cart_items':cart_items
    })


def add_cart_item(request, id):
    if not is_logged_in(request):
        return redirect('/login_view')
    
    user_id = request.session.get('user_id')
    cart, created = Cart.objects.get_or_create(user_id=user_id)

    food_item = FoodItem.objects.get(id=id)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, food_item=food_item)

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('item_details', id=id)

def reduce_cart_item(request, id):
    if not is_logged_in(request):
        return redirect('/login_view')
    
    user_id = request.session.get('user_id')
    cart = Cart.objects.filter(user_id=user_id).first()

    if not cart:
        return redirect('item_details', id=id)

    food_item = FoodItem.objects.get(id=id)
    cart_item = CartItem.objects.filter(cart=cart, food_item=food_item).first()

    if cart_item:
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()

    return redirect('item_details', id=id)


def fetch_add_cart_item(request, id):
    if not is_logged_in(request):
        return JsonResponse({'error': 'Unauthorized'}, status=401)
    
    user_id = request.session.get('user_id')
    cart, created = Cart.objects.get_or_create(user_id=user_id)

    food_item = FoodItem.objects.get(id=id)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, food_item=food_item)

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return JsonResponse({'quantity': cart_item.quantity,
                         'name': food_item.name,
                         'price': food_item.price,})


def fetch_reduce_cart_item(request, id):
    if not is_logged_in(request):
        return JsonResponse({'error': 'Unauthorized'}, status=401)
    
    user_id = request.session.get('user_id')
    cart = Cart.objects.filter(user_id=user_id).first()

    if not cart:
        return JsonResponse({'error': 'Cart not found'}, status=404)

    food_item = FoodItem.objects.get(id=id)
    cart_item = CartItem.objects.filter(cart=cart, food_item=food_item).first()

    if cart_item:
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
            return JsonResponse({'quantity': cart_item.quantity})
        else:
            cart_item.delete()
            return JsonResponse({'quantity': 0})

    return JsonResponse({'error': 'Cart item not found'}, status=404)

def place_order(request):
    if not is_logged_in(request):
        return redirect('/login_view')
    user = User.objects.get(id=request.session.get('user_id'))
    cart = Cart.objects.get(user=user)
    cart_items = CartItem.objects.filter(cart=cart)

    if not cart_items.exists():
        return redirect('cart_view')

    order = Order.objects.create(user=user, total_price=0)

    total = 0

    for item in cart_items:
        OrderItem.objects.create(
            order=order,
            food_item=item.food_item,
            quantity=item.quantity
        )
        total += item.quantity * item.food_item.price

    order.total_price = total
    order.save()

    cart_items.delete()

    return redirect('/order_summary/4')


def order_summary(request, order_id):
    if not is_logged_in(request):
        return redirect('/login_view')
    
    order = Order.objects.get(id=order_id)
    order_items = OrderItem.objects.filter(order=order).select_related('food_item')

    return render(request, 'order_summary.html', {
        'order': order,
        'order_items': order_items
    })


def user_order(request):
    if not is_logged_in(request):
        return redirect('/login_view')
    
    orders = Order.objects.filter(user_id=request.session.get('user_id'), status__in=['pending', 'preparing','out for delivery'])
    orderItem = OrderItem.objects.filter(order__in=orders).select_related('food_item')
    return render(request,'user_order.html', {'orders': orders, 'orderItems': orderItem})


def user_order_history(request):
    if not is_logged_in(request):
        return redirect('/login_view')
    

    return render(request,'user_order_history.html')


#Managers Views
def manager(request):
    if not is_logged_in(request):
        return redirect('/login_view')
    

    return render(request,'manager.html')


def current_orders(request):
    if not is_logged_in(request):
        return redirect('/login_view')
    

    return render(request,'current_orders.html')


def categories(request):
    if not is_logged_in(request):
        return redirect('/login_view')
    
    
    return render(request,'categories.html')


def food_items(request):
    if not is_logged_in(request):
        return redirect('/login_view')
    
    if request.session.get('role') != 'manager':
        return HttpResponse('Unauthorized')
    
    categories = Category.objects.all()
    food_items = FoodItem.objects.select_related('category').all()

    return render(request,'food_items.html',{
        'categories':categories,
        'food_items':food_items
    })


def room_view(request):
    if not is_logged_in(request):
        return redirect('/login_view')
    return render(request,'room_view.html')

def orders_history(request):
    if not is_logged_in(request):
        return redirect('/login_view')
    return render(request,'orders_history.html')

def add_food_item(request):
    if not is_logged_in(request):
        return redirect('/login_view')
    
    if request.session.get('role') != 'manager':
        return HttpResponse('Unauthorized')
    

    if request.method == 'POST':
        name = request.POST.get('name')
        price = request.POST.get('price')
        description = request.POST.get('description')
        category_id = request.POST.get('category')
        category = Category.objects.get(id=category_id)
        image = request.FILES.get('image')

        FoodItem.objects.create(
            name = name,
            price = price,
            description = description,
            category = category,
            image = image
        )
        return redirect('/add_food_item')

    categories = Category.objects.all()
    return render(request,'add_food_item.html',{'categories':categories})

def edit_item(request,id):
    if not is_logged_in(request):
        return redirect('/login_view')
    item = FoodItem.objects.get(id=id)

    if request.session.get('role') != 'manager':
        return HttpResponse('Unauthorized')
    
    if request.method == 'POST':
        item.name = request.POST.get('name')
        item.price = request.POST.get('price')
        item.description = request.POST.get('description')
        item.is_available = request.POST.get('is_available') == 'on'

        if(request.FILES.get('image')):
            item.image = request.FILES.get("image")
        
        item.save()
        return redirect('editItem', id=id)

    return render(request,'edit_item.html',{
        'item':item
    })


def delete_item(request,id):
    if not is_logged_in(request):
        return redirect('/login_view')
    
    if request.session.get('role') != 'manager':
        return HttpResponse('Unauthorized')
    
    item = FoodItem.objects.get(id=id)
    item.delete()

    # if request.method == 'POST'
    return redirect('/food_items')
