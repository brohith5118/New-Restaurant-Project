from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import User,Category,Order,OrderItem,FoodItem

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

    return render(request,'item_details.html',{
        'foodItem':food_item
    })


def user_order(request):
    if not is_logged_in(request):
        return redirect('/login_view')
    

    return render(request,'user_order.html')


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
